##*
## MIT License
##
## NNMeta - Copyright (c) 2020-2021 Aleksandr Kazakov <alexander.d.kazakov|at|gmail.com>
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.
##*

from dataclasses import dataclass, field
from typing      import List, Dict, Any, Callable

import os, sys, shutil, re
from collections import defaultdict
from ase         import Atoms
from ase.io      import read, write
from ase.units   import Bohr,kJ,Hartree,mol,kcal

import torch
import numpy   as np
import nnpackage as pack

from torch                     import Tensor
from nnpackage.atomistic.model import AtomisticModel
from nnpackage                 import AtomsLoader, AtomsData
from nnpackage.train.metrics   import MeanAbsoluteError, RootMeanSquaredError, MeanSquaredError
from nnpackage.train           import Trainer, CSVHook, ReduceLROnPlateauHook
from nnpackage.train           import build_mse_loss, build_mae_loss, build_sae_loss
from storer                    import Storer

import copy
import warnings
warnings.filterwarnings("ignore")

from tqdm import tqdm
if tqdm: print_function = tqdm.write
else:    print_function = print

from subprocess import Popen, PIPE
import xml.etree.ElementTree as ET


DM = {
    0 : "dipole_moment_x",
    1 : "dipole_moment_y",
    2 : "dipole_moment_z",
}

AVAILABLE_ENERGY_UNITS     = ("hartree", "kj/mol", "kcal/mol", "ev",)
AVAILABLE_FORCE_UNITS      = ("bohr", "angstrom")
AVAILABLE_DM_UNITS         = ("debye",)
AVAILABLE_KEYS_NN_SETTINGS = ("index_epochs", "index_epochs_weight", "weight")


CONVERTER = {
    # ENERGY
    # from
    "hartree" : {
        # to
        "hartree":  1.,                  # assuming input energy as Hartree
        "kcal/mol": Hartree * mol/kcal,  # ~ 627.5094
        "kj/mol":   Hartree * mol/kJ,    # ~ 2625.4996
        "ev":       Hartree,             # ~ 27.2114
    },
    # FORCE
    # from
    "hartree/bohr" : {
        # to
        "hartree/bohr":  1.,                  # assuming input force as Hartree/Bohr
        "kcal/mol/bohr": Hartree * mol/kcal,  # ~ 627.5094
        "kj/mol/bohr":   Hartree * mol/kJ,    # ~ 2625.4996
        "ev/bohr":       Hartree,             # ~ 27.2114
        # angstrom
        "hartree/angstrom":  Bohr * 1.,                  # assuming input force as Hartree/Bohr
        "kcal/mol/angstrom": Bohr * Hartree * mol/kcal,  # ~ 332.0637
        "kj/mol/angstrom":   Bohr * Hartree * mol/kJ,    # ~ 1389.3545
        "ev/angstrom":       Bohr * Hartree,             # ~ 14.3996
    },
    # DIPOLE_MOMENT
    # from
    "debye" : {
        # to
        "debye":  1.,                  # assuming input DM as Debye
    },
}

@dataclass
class GPUInfo:
    """
    It provides information about GPU utilization and GPU availability.

    """
    gpus       : List = field(default_factory=list)
    idx_in_use : List = field(default_factory=list)
    notified   : int  = 0
    _no_nvidia : bool = False

    def get_info(self):
        self.gpus.clear()

        try: p = Popen(["nvidia-smi", "-q", "-x"], stdout=PIPE)
        except Exception as e:
            if not self._no_nvidia:
                print(f"No nvidia-smi? {e}")
                self.gpus.clear()
                self._no_nvidia = True
            return

        outs, errors = p.communicate()
        root = ET.fromstring(outs)

        num_gpus = int(root.find("attached_gpus").text)
        for gpu_id, gpu in enumerate(root.iter("gpu")):
            gpu_info = dict()
            # idx and name
            gpu_info["idx"] = gpu_id
            name = gpu.find("product_name").text
            gpu_info["name"] = name

            # GPU UUID
            gpu_uuid = gpu.find("uuid").text
            gpu_info["uuid"] = gpu_uuid

            # get memory
            memory_usage = gpu.find("fb_memory_usage")
            total = memory_usage.find("total").text
            used  = memory_usage.find("used").text
            free  = memory_usage.find("free").text
            gpu_info["memory"] = dict(total = total, used = used, free = free)

            # get utilization
            utilization = gpu.find("utilization")
            gpu_util    = utilization.find("gpu_util").text
            memory_util = utilization.find("memory_util").text
            gpu_info["utilization"] = dict(gpu_util = gpu_util, memory_util = memory_util)

            # processes
            processes = gpu.find("processes")
            infos = []
            for info in processes.iter("process_info"):
                pid          = info.find("pid").text
                process_name = info.find("process_name").text
                process_type = info.find("type").text
                used_memory  = info.find("used_memory").text
                infos.append(dict(pid = pid, process_name = process_name, process_type = process_type, used_memory = used_memory))
            gpu_info["processes"] = infos
            self.gpus.append(gpu_info)

    def __post_init__(self):
        self.get_info()

    def notify(self, about_in_use_only:bool = False):
        self.get_info()
        idx_in_use = self.get_gpu_in_use()
        for gpu in self.gpus:
            notify_string = f"ID:{gpu['idx']} | NAME:{gpu['name']} | MEMORY: {gpu['memory']['used']:>10} / {gpu['memory']['total']:<10} | JOBS: {len(gpu['processes'])}"
            if gpu['idx'] in idx_in_use:
                if not about_in_use_only: notify_string += " <--- in USE"
                else: print_function(notify_string)
            if not about_in_use_only: print_function(notify_string)

    def get_gpu_in_use(self) -> List:
        """
        Returns GPU indexes: either visible devices or free of task

        """
        if not self.idx_in_use:
            idx = []
            try:             visible_gpu = os.environ["CUDA_VISIBLE_DEVICES"].split(",")
            except KeyError: visible_gpu = self.get_empty_gpu()
            if len(visible_gpu) == 0: visible_gpu = self.get_empty_gpu_excluded_G_jobs()

            for gpu in self.gpus:
                # uuid/ idx
                if gpu["uuid"] in visible_gpu or str(gpu["idx"]) in visible_gpu: idx.append(gpu["idx"])
            self.idx_in_use = idx
        else:
            idx = self.idx_in_use
        return idx

    def get_empty_gpu(self)  -> List:
        """
        return indexes of free task GPU

        """
        idx = []
        for gpu in self.gpus:
            if len(gpu["processes"]) == 0: idx.append(gpu["idx"])
        if len(idx) == 0:
            if self.notified < 2:
                print("[Warning!] No empty devices!");
                self.notified += 1
        return idx

    def get_empty_gpu_excluded_G_jobs(self) -> List:
        """
        return indexes of G type free task GPU

        """
        idx = []
        for gpu in self.gpus:
            g_type_process_jobs = 0
            for job in gpu["processes"]:
                if job["process_type"].upper() == "G": g_type_process_jobs += 1
            number_jobs_without_g_type = len(gpu["processes"]) - g_type_process_jobs
            if number_jobs_without_g_type == 0: idx.append(str(gpu["idx"]))
        if len(idx) == 0:
            if self.notified < 2:
                print("[Warning!] No empty devices even without G type jobs!")
                self.notified += 1
        return idx

@dataclass
class NNClass:
    __version__                  : str            = "2.0.1"
    debug                        : bool           = False
    _should_train                : bool           = True
    _force_gpu                   : bool           = False
    _force_map                   : List[int]      = None
    _index_epoch_weight_key      : Dict           = field(default_factory=dict)

    internal_name                : str            = "[NNClass]"
    system_path                  : str            = "."
    plot_enabled                 : bool           = False
    mean_std_use                 : bool           = True
    meta                         : bool           = True
    storer                       : object         = None
    device                       : str            = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    network_name                 : str            = "unknower"
    info                         : dict           = field(default_factory=dict)
    gpu_info                     : GPUInfo        = GPUInfo()
    #
    db_properties                : tuple          = ("energy", "forces", "dipole_moment")  # properties look for database
    training_properties          : tuple          = ("energy", "forces", "dipole_moment")  # properties used for training
    nn_settings                  : dict           = field(default_factory=dict)
    training_progress            : dict           = field(default_factory=dict)
    loss_function_choice         : str            = "mse" # Available: ["mse", "mae", "sae", .?.]
    loss_fun_builder             : Callable       = None
    #
    redo_split_file              : bool           = False
    foreign_plotted              : bool           = False
    loss_tradeoff                : tuple          = (0.2, 0.8, 0.5)
    lr                           : np.float64     = 1e-4
    predict_each_epoch           : int            = 10
    validate_each_epoch          : int            = 10

    batch_size                   : int            = 16
    n_features                   : int            = 128
    n_filters                    : int            = 128
    n_gaussians                  : int            = 25
    n_interactions               : int            = 1
    cutoff                       : int            = 5.0  # angstroms

    n_layers_energy_force        : int            = 2
    n_layers_dipole_moment       : int            = 2
    n_neurons_energy_force       : int            = None
    n_neurons_dipole_moment      : int            = None
    _n_output_dipole_moment      : int            = 3
    is_dipole_moment_magnitude   : bool           = False

    #
    using_matplotlib             : bool           = False
    compare_with_foreign_model   : bool           = False
    # visualize_points_from_nn     : int            = 100  # DEPRECATED // REMOVE IN NEXT VERSION
    visualize_points_from_data   : int            = 100
    #
    samples                      : List[Atoms]    = None
    model                        : AtomisticModel = None
    trainer                      : Trainer        = None
    train_loader                 : AtomsLoader    = None
    valid_loader                 : AtomsLoader    = None
    test_loader                  : AtomsLoader    = None

    train_samples                : np.array       = None
    valid_samples                : np.array       = None
    test_samples                 : np.array       = None

    train_samples_percent        : np.float64     = 60.0
    valid_samples_percent        : np.float64     = 20.0
    _number_train_samples        : int            = 0
    _number_valid_samples        : int            = 0
    units = dict(
        ENERGY        = "Hartree",
        FORCE         = "Hartree/Bohr",
        DIPOLE_MOMENT = "Debye"
    )

    # Downsampler
    downsample_each_epoch        : int            = -1   # Turned off
    downsample_threshold         : float          = None # Turned off

    check_list_files             : dict          = field(default_factory=dict)

    def __post_init__(self):
        if self.system_path[-1] != "/": self.system_path+="/"
        #
        self.xyz_path              = os.path.expanduser(self.system_path) + "xyz/"
        self.db_path               = os.path.expanduser(self.system_path) + "dbs/"
        self.general_models_path   = os.path.expanduser(self.system_path) + "models/"
        self.split_path            = os.path.expanduser(self.system_path) + "splits/"
        self.test_path             = os.path.expanduser(self.system_path) + "tests/"
        self.path2foreign_model    = os.path.expanduser(self.system_path) + "foreign_model/"
        #
        os.makedirs(os.path.dirname(self.db_path),             exist_ok=True)
        os.makedirs(os.path.dirname(self.general_models_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.split_path),          exist_ok=True)
        os.makedirs(os.path.dirname(self.test_path),           exist_ok=True)

        # info
        kf = self.network_name+"_features"
        try:
            _ = self.info[self.network_name]
        except KeyError:
            available_nns = []
            for k in self.info:
                if not str(k).endswith("_features"): available_nns.append(k)

            print_function(f"There is no information about [{self.network_name}] network in `info`")
            print_function(f"Known NNs: {available_nns}")
            sys.exit(1)

        self.nn_settings = self.info[self.network_name]

        if self.info[kf].get("_should_train")              is not None: self._should_train               = self.info[kf].get("_should_train")
        if self.info[kf].get("_force_gpu")                 is not None: self._force_gpu                  = self.info[kf].get("_force_gpu")
        if self.info[kf].get("_force_map")                 is not None: self._force_map                  = self.info[kf].get("_force_map")
        if self.info[kf].get("device")                     is not None: self.device                      = torch.device(self.info[kf].get("device"))
        if self.info[kf].get("is_dipole_moment_magnitude") is not None: self.is_dipole_moment_magnitude  = self.info[kf].get("is_dipole_moment_magnitude")
        if self.info[kf].get("predict_each_epoch"):                     self.predict_each_epoch          = self.info[kf].get("predict_each_epoch")
        if self.info[kf].get("validate_each_epoch"):                    self.validate_each_epoch         = self.info[kf].get("validate_each_epoch")
        if self.info[kf].get("lr"):                                     self.lr                          = self.info[kf].get("lr")
        if self.info[kf].get("batch_size"):                             self.batch_size                  = self.info[kf].get("batch_size")
        if self.info[kf].get("n_features"):                             self.n_features                  = self.info[kf].get("n_features")
        if self.info[kf].get("n_filters"):                              self.n_filters                   = self.info[kf].get("n_filters")
        if self.info[kf].get("n_interactions"):                         self.n_interactions              = self.info[kf].get("n_interactions")
        if self.info[kf].get("n_gaussians"):                            self.n_gaussians                 = self.info[kf].get("n_gaussians")
        if self.info[kf].get("cutoff"):                                 self.cutoff                      = self.info[kf].get("cutoff")
        if self.info[kf].get("db_properties"):                          self.db_properties               = self.info[kf].get("db_properties")
        if self.info[kf].get("training_properties"):                    self.training_properties         = self.info[kf].get("training_properties")
        if self.info[kf].get("loss_tradeoff"):                          self.loss_tradeoff               = self.info[kf].get("loss_tradeoff")
        if self.info[kf].get("mean_std_use"):                           self.mean_std_use                = self.info[kf].get("mean_std_use")

        if self.info[kf].get("n_layers_energy_force"):                  self.n_layers_energy_force       = self.info[kf].get("n_layers_energy_force")
        if self.info[kf].get("n_neurons_energy_force"):                 self.n_neurons_energy_force      = self.info[kf].get("n_neurons_energy_force")

        if self.info[kf].get("n_layers_dipole_moment"):                 self.n_layers_dipole_moment      = self.info[kf].get("n_layers_dipole_moment")
        if self.info[kf].get("n_neurons_dipole_moment"):                self.n_neurons_dipole_moment     = self.info[kf].get("n_neurons_dipole_moment")

        if self.info[kf].get("train_samples_percent"):                  self.train_samples_percent       = self.info[kf].get("train_samples_percent")
        if self.info[kf].get("valid_samples_percent"):                  self.valid_samples_percent       = self.info[kf].get("valid_samples_percent")

        if self.info[kf].get("visualize_points_from_data"):             self.visualize_points_from_data  = self.info[kf].get("visualize_points_from_data")

        if self.info[kf].get("check_list_files"):                       self.check_list_files            = self.info[kf].get("check_list_files")
        if self.info[kf].get("loss_function_choice"):                   self.loss_function_choice        = self.info[kf].get("loss_function_choice")
        if self.info[kf].get("units"):                                  self.units                       = self.info[kf].get("units")
        #
        if self.info[kf].get("downsample_each_epoch"):                  self.downsample_each_epoch       = self.info[kf].get("downsample_each_epoch")
        if self.info[kf].get("downsample_threshold"):                   self.downsample_threshold        = self.info[kf].get("downsample_threshold")


        self.check_provided_parameters()
        self._import_relevant_loss()
        print_function(f"{self.internal_name} [v.{self.__version__}] | System path: {self.system_path}")
        if self.debug: print_function(f"<<<Debug call>>>\n {str(self)}"); sys.exit(0)

        if self.plot_enabled:
            try:
                from vplotter import Plotter
                self.using_matplotlib = False
            except:
                print_function(f"Sorry. Plotter is not available. Matplotlib will be in use...")
                import matplotlib.pyplot as plt
                self.using_matplotlib = True

        if not self.using_matplotlib and self.plot_enabled:

            pages_info = dict()
            if "energy" in self.training_properties:
                pages_info["delta_energy"] = dict(xname="[sample number]" , yname=f"\\Delta Energy [{self.units['ENERGY']}]",)
                pages_info["xyz_file"]     = dict(xname="[sample number]" , yname=f"Energy [{self.units['ENERGY']}]",)
                pages_info["xyz_file_sub"] = dict(xname="[sample number]" , yname=f"Energy-(int)E[0], [{self.units['ENERGY']}]",)
                pages_info["diag_energy"]  = dict(xname=f"Energy [orig], [{self.units['ENERGY']}]",
                                                  yname=f"Energy [pred], [{self.units['ENERGY']}]",)
                pages_info["diag_energy_norm"]  = dict(xname=f"Energy/atom [orig], [{self.units['ENERGY']}]",
                                                  yname=f"Energy/atom [pred], [{self.units['ENERGY']}]",)
                pages_info["energy_loss_per_sample"]        = dict(xname="[sample number]" , yname=f"\\Delta Energy = Pred - Orig, [{self.units['ENERGY']}]", )
                pages_info["energy_loss_per_sample_inside"] = dict(xname="[sample number]" , yname="\\Delta Energy_{inside} = Pred - Orig, "f"[{self.units['ENERGY']}]", )

                # framework
                pages_info["energy_loss"]  = dict(xname="Time [s]", yname=f"Energy LOSS [{self.units['ENERGY']}]", xlog=True, ylog=True)
                pages_info["forces_loss"]  = dict(xname="Time [s]", yname=f"Force  LOSS [{self.units['FORCE']}]" , xlog=True, ylog=True)

            if "dipole_moment" in self.training_properties or "dipole_moment_magnitude" in self.training_properties:
                # framework
                pages_info["dipole_moment_loss"]    = dict(xname="[sample number]", yname=f"Dipole moment LOSS [{self.units['DIPOLE_MOMENT']}]",)
                #
                if self.is_dipole_moment_magnitude:
                    pages_info["dipole_moment_magnitude"]       = dict(xname="[sample number]", yname=f"Dipole moment [magnitude] [{self.units['DIPOLE_MOMENT']}]",)
                    pages_info["diag_dp_magnitude"]             = dict(xname=f"Dipole moment [magnitude] [orig] [{self.units['DIPOLE_MOMENT']}]",
                                                                       yname=f"Dipole moment [magnitude] [pred] [{self.units['DIPOLE_MOMENT']}]")
                    pages_info["delta_dipole_moment_magnitude"] = dict(xname="[sample number]",
                                                                       yname=f"\\Delta Dipole moment [magnitude] [{self.units['DIPOLE_MOMENT']}]",)
                else:
                    pages_info["dipole_moment_x"]       = dict(xname="[sample number]", yname=f"Dipole moment [x] [{self.units['DIPOLE_MOMENT']}]",)
                    pages_info["dipole_moment_y"]       = dict(xname="[sample number]", yname=f"Dipole moment [y] [{self.units['DIPOLE_MOMENT']}]",)
                    pages_info["dipole_moment_z"]       = dict(xname="[sample number]", yname=f"Dipole moment [z] [{self.units['DIPOLE_MOMENT']}]",)
                    #
                    pages_info["diag_dp_x"]             = dict(xname=f"Dipole moment [x] [orig] [{self.units['DIPOLE_MOMENT']}]",
                                                               yname=f"Dipole moment [x] [pred] [{self.units['DIPOLE_MOMENT']}]")
                    pages_info["diag_dp_y"]             = dict(xname=f"Dipole moment [y] [orig] [{self.units['DIPOLE_MOMENT']}]",
                                                               yname=f"Dipole moment [y] [pred] [{self.units['DIPOLE_MOMENT']}]")
                    pages_info["diag_dp_z"]             = dict(xname=f"Dipole moment [z] [orig] [{self.units['DIPOLE_MOMENT']}]",
                                                               yname=f"Dipole moment [z] [pred] [{self.units['DIPOLE_MOMENT']}]")

                    pages_info["delta_dipole_moment_x"] = dict(xname="[sample number]",
                                                               yname=f"\\Delta Dipole moment [x] [{self.units['DIPOLE_MOMENT']}]",)
                    pages_info["delta_dipole_moment_y"] = dict(xname="[sample number]",
                                                               yname=f"\\Delta Dipole moment [y] [{self.units['DIPOLE_MOMENT']}]",)
                    pages_info["delta_dipole_moment_z"] = dict(xname="[sample number]",
                                                               yname=f"\\Delta Dipole moment [z] [{self.units['DIPOLE_MOMENT']}]",)

            self.plotter_progress = Plotter(title="Check Results", pages_info=pages_info, keyFontSize = 8)
            #self.plotter_log      = Plotter(title="", engine="gnuplot")  # TODO: Gnuplot stabilization


    def check_provided_parameters(self) -> None:
        ok = True; mess = ""
        # 1
        if (self.train_samples_percent + self.valid_samples_percent) >= 100:
            ok, mess = False, "Training[%] + Validation[%] have to be smaller than 100% | The rest samples are for tests purpose."
        if not ok: print_function(mess); sys.exit(1)
        # 2
        # units
        if self.units["ENERGY"].lower() in AVAILABLE_ENERGY_UNITS:              ok1 = True;  mess1 = ""
        else:                                                                   ok1 = False; mess1 = f"Not available energy units [{self.units['ENERGY']}];"
        if self.units["FORCE"].split("/")[-1].lower() in AVAILABLE_FORCE_UNITS: ok2 = True;  mess2 = ""
        else:                                                                   ok2 = False; mess2 = f"Not available force units [{self.units['FORCE']}];"
        if self.units["DIPOLE_MOMENT"].lower() in AVAILABLE_DM_UNITS:           ok3 = True;  mess3 = ""
        else:                                                                   ok3 = False; mess3 = f"Not available dipole moment units [{self.units['DIPOLE_MOMENT']}];"
        ok   = ok1 and ok2 and ok3
        mess = mess1 + mess2 + mess3
        if not ok: print_function(mess); sys.exit(1)
        # 3
        for fs in self.nn_settings:
            _keys = self.nn_settings[fs].keys()
            for _key in _keys:
                if _key not in AVAILABLE_KEYS_NN_SETTINGS:
                    ok, mess = False, f"Such key [{_key}] is not available. Consider from: {AVAILABLE_KEYS_NN_SETTINGS}"
                    if not ok: print_function(mess); sys.exit(1)
            # cross
            if "index_epochs" in _keys and "index_epochs_weight" in _keys:
                ok, mess = False, f"It is not allowed to use both 'index_epochs' and 'index_epochs_weight' at the same time."
                if not ok: print_function(mess); sys.exit(1)
            #
            #
            if   "index_epochs"        in _keys: right_key = "index_epochs"
            elif "index_epochs_weight" in _keys: right_key = "index_epochs_weight"
            else:
                ok, mess = False, f"You need provide either 'index_epochs' or 'index_epochs_weight' key for start training."
                if not ok: print_function(mess); sys.exit(1)
            self._index_epoch_weight_key[fs] = right_key

    def _import_relevant_loss(self) -> None:
        if   self.loss_function_choice == "mse": self.loss_fun_builder = build_mse_loss
        elif self.loss_function_choice == "mae": self.loss_fun_builder = build_mae_loss
        elif self.loss_function_choice == "sae": self.loss_fun_builder = build_sae_loss
        else:
            print(f"Waring! Loss function choice is not covered, MSE loss function will be in use!\n [Your choice is {self.loss_function_choice}]...")
            self.loss_fun_builder = build_mse_loss

# DEPRECATED // REMOVE IN NEXT VERSION
    @staticmethod
    def loss_function(batch: Any, result: Any) -> Tensor:
        # tradeoff
        rho_tradeoff = 0.1
        # compute the mean squared error on the energies
        diff_energy = batch["energy"]-result["energy"]
        err_sq_energy = torch.mean(diff_energy**2)

        # compute the mean squared error on the forces
        diff_forces = batch["forces"]-result["forces"]
        err_sq_forces = torch.mean(diff_forces**2)

        # build the combined loss function
        err_sq = rho_tradeoff*err_sq_energy + (1-rho_tradeoff)*err_sq_forces

        return err_sq

    @staticmethod
    def find_dbs(db_path: Any) -> List:
        db_list = []
        for db_file in os.listdir(db_path):
            if db_file.endswith(".db"):
                db_fname = os.fsdecode(db_file)
                print_function(f"     Found: {db_fname}")
                db_list.append(db_fname)
        return db_list

    def _get_db_name(self, xyz_file: str,  indexes: str) -> str:
            return f"{xyz_file}_{str(indexes)}_{self.units['ENERGY'].replace('/','')}_{self.units['FORCE'].replace('/','')}_{self.units['DIPOLE_MOMENT'].replace('/','')}.db"

    def print_info(self) -> None:
        print_function(f"""
# # # # # # # # # # # [INFORMATION [{self.network_name}] | device {self.device.type} | GPU idx: {self.gpu_info.get_gpu_in_use()}] # # # # # # # # # # #
        NUMBER TRAINING EXAMPLES  [%]/# :   {self.train_samples_percent}/{self._number_train_samples}
        NUMBER VALIDATION EXAMPLES[%]/# :   {self.valid_samples_percent}/{self._number_valid_samples}
        LEARNING RATE                   :   {self.lr}
        N INTERACTION                   :   {self.n_interactions}
        LOSS TRADEOFF                   :   {self.loss_tradeoff}
        LOSS FUNCTION CHOICE            :   {self.loss_function_choice}
        TRAINING PROPERTIES             :   {self.training_properties}

        ENERGY UNITS                    :   [{self.units["ENERGY"]}]
        FORCE UNITS                     :   [{self.units["FORCE"]}]
        DIPOLE MOMENT UNITS             :   [{self.units["DIPOLE_MOMENT"]}]
            DIPOLE_MOMENT MAGNITUDE     :   [{self.is_dipole_moment_magnitude}]

        DB INFO:
            PROPERTIES                  :   {self.db_properties}

        PATHS:
            XYZ                         :   {self.xyz_path}
            DB                          :   {self.db_path}
            MODEL [GENERAL]             :   {self.general_models_path}
            SPLITS                      :   {self.split_path}

        NN SETTINGS:
            {self.nn_settings}

        """)
        self.storer.show()

    def create_model_path(self, redo:bool = False) -> None:
        self.model_path   = self.general_models_path + self.network_name

        if redo:
            ans = input("Are you sure with removing the trained model? [y/N]\n")
            if ans == "y":
                print_function(
                    """
                    REMOVING THE PREVIOUS MODEL (IF EXIST) + TEST_FOLDER

                    """
                )
                # before setting up the trainer, remove previous model and tests
                try: shutil.rmtree(self.model_path)
                except FileNotFoundError: pass
                try: shutil.rmtree(self.test_path + self.network_name)
                except FileNotFoundError: pass
            else:
                print_function(f"Skipping removing...")

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        self.storer  = Storer(dump_name=self.network_name, dump_path=self.model_path, compressed=False)

    def validate(self) -> None:
        """
        Plotting the training progress by the framework.

        """

        energy_loss, forces_loss, = torch.Tensor(np.array([0.])), torch.tensor(np.array([[0., 0., 0.], [0., 0., 0.]]))
        if self.is_dipole_moment_magnitude:  dipole_moment_loss = torch.Tensor(np.array([0.]))
        else:                                dipole_moment_loss = torch.tensor(np.array([[0., 0., 0.], [0., 0., 0.]]))

        with open(os.path.join(self.model_path, 'log.csv')) as flog: head = [next(flog) for line in range(1)]
        titles = head[0].strip().lower().split(",")
        # Load logged results
        results = np.loadtxt(os.path.join(self.model_path, 'log.csv'), skiprows=1, delimiter=',')

        self.training_progress.clear()  # clear before use
        for idx, title in enumerate(titles): self.training_progress[title] = results[:, idx]

        # Determine time axis
        time = results[:,0]-results[0,0]
        time_ = self.training_progress['time'] - self.training_progress['time'][0]

        # Load the validation MAEs
        if 'energy'                  in self.training_properties: energy_loss        = self.training_progress['energy']
        if 'forces'                  in self.training_properties: forces_loss        = self.training_progress['forces']
        if 'dipole_moment'           in self.training_properties: dipole_moment_loss = self.training_progress['dipole_moment']
        if "dipole_moment_magnitude" in self.training_properties: dipole_moment_loss = self.training_progress['dipole_moment_magnitude']


        # Get final validation errors
        print_function(f"""

Validation LOSS | epochs {self.storer.get(self.name4storer)}:
          <energy> [{self.units['ENERGY']}]: {str(energy_loss[-1]):>25}
          <forces> [{self.units['FORCE']}]: {str(forces_loss[-1]):>15}
          <dipole moment> [{self.units['DIPOLE_MOMENT']}]: {str(dipole_moment_loss[-1]):>15}

        """)

        if self.meta: return
        else:
            if not self.using_matplotlib:
                if 'energy'        in self.training_properties: self.plotter_progress.plot(x=time, y=energy_loss,        key_name="", page="energy_loss")
                if 'forces'        in self.training_properties: self.plotter_progress.plot(x=time, y=forces_loss,        key_name="", page="forces_loss")
                if 'dipole_moment' in self.training_properties or 'dipole_moment_magnitude' in self.training_properties:
                    self.plotter_progress.plot(x=time, y=dipole_moment_loss, key_name="", page="dipole_moment_loss")
            else:
                # Matplotlib instructions
                plt.figure(figsize=(14,5))

                # Plot energies
                plt.subplot(1,2,1)
                plt.plot(time, energy_loss)
                plt.title("Energy")
                plt.ylabel("Energy LOSS [{self.units['ENERGY']}]")
                plt.xlabel("Time [s]")

                # Plot forces
                plt.subplot(1,2,2)
                plt.plot(time, forces_loss)
                plt.title("Forces")
                plt.ylabel("Force LOSS [{self.units['FORCE']}]")
                plt.xlabel("Time [s]")
                plt.show()

    def prepare_databases(self, redo:bool = False, index:str = "0:10:10", xyz_file:str = "noname.xyz") -> None:
        # recreating databases
        if redo:
            db_list = NNClass.find_dbs(db_path=self.db_path)
            print_function(f"{self.internal_name} [Re-creating databases...]")
            for db_fname in db_list:
                os.remove(self.db_path + db_fname)
                print_function(f"     {db_fname} removed.")

        print_function(f"{self.internal_name} Checking databases...")
        db_fname      = self._get_db_name(xyz_file=xyz_file, indexes=index)
        db_path_fname = os.path.join(self.db_path, db_fname)

        if os.path.exists(db_path_fname): print_function(f" ==> {db_fname} [OK]")
        else:
            # no databases is found
            print_function(f"{self.internal_name} Preparing databases...")
            print_function(f"Creating {db_path_fname} with indexes: {index}")
            property_list = []
            samples = read(self.xyz_path + xyz_file, index=index, format="extxyz")
            for sample in tqdm(samples, "Preparing database..."):
                # All properties need to be stored as numpy arrays
                # Note: The shape for scalars should be (1,), not ()
                # Note: GPUs work best with float32 data
                # Note: BE SURE if results are not suffer from lack of precision.
                _ = dict()
                if 'energy' in self.db_properties:
                    try:
                        # assume energy comes in [Hartree]
                        energy = np.array([sample.info['energy']], dtype=np.float64); _['energy'] = CONVERTER["hartree"][self.units['ENERGY'].lower()] * energy
                    except Exception as e: print_function(f"[Warning]: {e}")
                if 'forces' in self.db_properties:
                    try:
                        # assume force comes in [Hartree/Borh]
                        forces = np.array(sample.get_forces(),   dtype=np.float64); _['forces'] = CONVERTER["hartree/bohr"][self.units['FORCE'].lower()] * forces
                    except Exception as e: print_function(f"[Warning]: {e}")
                if 'dipole_moment' in self.db_properties:
                    try:
                        # assume dipole moment comes in [Debye]
                        dipole_moment = np.array(sample.get_dipole_moment(), dtype=np.float64)
                        _['dipole_moment'] = CONVERTER["debye"][self.units["DIPOLE_MOMENT"].lower()] * dipole_moment
                    except Exception as e: print_function(f"[Warning]: {e}")
                if 'dipole_moment_magnitude' in self.db_properties:
                    try:
                        dipole_moment = np.array(sample.get_dipole_moment(), dtype=np.float64)
                        _['dipole_moment_magnitude'] = np.array([np.linalg.norm(dipole_moment)], dtype=np.float64)
                    except Exception as e: print_function(f"[Warning]: {e}")
                property_list.append(_)

            # Creating DB
            new_dataset = AtomsData(db_path_fname, available_properties=self.db_properties)
            new_dataset.add_systems(samples, property_list)

            print_function(f"Creating databases for {self.xyz_path} is done!")

    def prepare_train_valid_test_samples(self, db_name:str = "xyzname.xyz_indexes.db") -> None:
        print_function(f"{self.internal_name} Preparing train/valid/test samples...")

        # loading db
        db_path_fname = self.db_path + db_name
        print_function(f"Loading... | {db_path_fname}")
        self.samples = AtomsData(db_path_fname, load_only=self.training_properties)  # pick the db

        # take first atoms/props
        atoms, props = self.samples.get_properties(idx=0)
        print_function(f"->>> 1 sample[{atoms.symbols}]")
        print('->>> [DB] Properties:\n', *[' -- {:s}\n'.format(key) for key in props.keys()])

        self._number_train_samples:int = int(len(self.samples) * (self.train_samples_percent / 100))
        self._number_valid_samples:int = int(len(self.samples) * (self.valid_samples_percent / 100))

        # creating path_file
        self.split_path_file = os.path.join(self.split_path, f"{db_name}_split_Ntrain{self._number_train_samples}_Nvalid{self._number_valid_samples}_{self.network_name}.npz")

        # removing if redo
        if self.redo_split_file:
            print_function(f"{self.internal_name} [Recreating split.npz]")
            try: os.remove(self.split_path_file)
            except FileNotFoundError: pass

        # split train validation testf
        self.train_samples, self.valid_samples, self.test_samples = pack.train_test_split(
            data       = self.samples,
            num_train  = self._number_train_samples,
            num_val    = self._number_valid_samples,
            split_file = self.split_path_file,  # WARNING! if the file exists it will be loaded.
        )

        print_function(f"{self.internal_name} Creating train/validation/test loader...")
        # PIN MEMORY <-?-> Savage of memory?
        self.train_loader = AtomsLoader(self.train_samples, batch_size=self.batch_size, num_workers=1, pin_memory=False, shuffle=True,)
        self.valid_loader = AtomsLoader(self.valid_samples, batch_size=self.batch_size, num_workers=1, pin_memory=False)
        self.test_loader  = AtomsLoader(self.test_samples,  batch_size=self.batch_size, num_workers=1, pin_memory=False)

        print_function(f"{self.internal_name} [train/valid/test] done.")

    def build_model(self) -> None:
        print_function(f"{self.internal_name} Checking the model...")
        map_location = self.device
        if len(self.gpu_info.get_gpu_in_use()) == 0: self.device = map_location =  torch.device("cpu")
        if self._force_gpu:
            self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
            if self.device.type == "cpu": print("[WARNING] Requested force GPU calculation, but the device is not available! Returning to cpu calculation mode..."); map_location = torch.device("cpu")
            if self._force_map is None: print("[WARNING] All available devices will be in use.");   map_location=torch.device("cuda")
            else:                       print(f"Next devices will be in use: [{self._force_map}]"); self.device = map_location=torch.device(f"cuda:{self._force_map[0]}");

        if os.path.exists(self.model_path + "/best_model"):
            print_function(f"{self.internal_name} Already trained network exists!")
            print_function(f"Loading [{self.device}]...")
            self.model = pack.utils.load_model(self.model_path + "/best_model", map_location=map_location)
            print_function(f"Model parameters: {self.model}")

        else:
            print_function(f"[WARNING] No neural network!")
            print_function(f"{self.internal_name} Building the model...")
            output_modules = []

            representation = pack.SchNet(
                n_atom_basis         = self.n_features,
                n_filters            = self.n_filters,
                n_interactions       = self.n_interactions,
                cutoff               = self.cutoff,
                n_gaussians          = self.n_gaussians,    # 25    -- default
                normalize_filter     = False,               # False -- default
                coupled_interactions = False,               # False -- default
                return_intermediate  = False,               # False -- default
                max_z                = 100,                 # 100   -- default
                charged_systems      = False,               # False -- default
                cutoff_network       = pack.nn.cutoff.CosineCutoff,
                )

            if "energy" in self.training_properties or "forces" in self.training_properties:

                per_atom = dict(energy=True, forces=False, dipole_moment=False)

                if not self.mean_std_use:
                    print_function("You requested not to use 'mean' and 'std' of energy")
                    means_energy  = None
                    stddevs_enegy = None

                else:
                    try:
                        means, stddevs = self.train_loader.get_statistics(
                            property_names  = list(self.training_properties),
                            divide_by_atoms = per_atom,
                            single_atom_ref = None
                        )
                        ## [0] !?!
                        print_function(f"Mean atomization energy      / atom: {means['energy']} [{self.units['ENERGY']}]")
                        print_function(f"Std. dev. atomization energy / atom: {stddevs['energy']} [{self.units['ENERGY']}]")
                        means_energy  = means  ["energy"]
                        stddevs_enegy = stddevs["energy"]
                    except Exception as e:
                        # Not consistent data: W2, W3, W$
                        print("[NOTE] Provided samples are not consistent!", e)
                        means_energy  = None
                        stddevs_enegy = None


                ENERGY_FORCE = pack.atomistic.Atomwise(
                    n_in             = representation.n_atom_basis,
                    n_out            = 1,                            # 1    -- default
                    aggregation_mode = "sum",                        # sum  -- default
                    n_layers         = self.n_layers_energy_force,   # 2    -- default
                    n_neurons        = self.n_neurons_energy_force,  # None -- default
                    property         = "energy",
                    derivative       = "forces",
                    mean             = means_energy,
                    stddev           = stddevs_enegy,
                    negative_dr      = True,
                )
                output_modules.append(ENERGY_FORCE)

            if "dipole_moment" in self.training_properties or "dipole_moment_magnitude" in self.training_properties:

                DIPOLE_MOMENT = pack.atomistic.DipoleMoment(
                    n_in              = representation.n_atom_basis,
                    n_out             = 1 if self.is_dipole_moment_magnitude else 3,
                    n_layers          = self.n_layers_dipole_moment,  # 2 -- default
                    n_neurons         = self.n_neurons_dipole_moment, # None -- default
                    activation        = pack.nn.activations.shifted_softplus,
                    property          = "dipole_moment_magnitude" if self.is_dipole_moment_magnitude else "dipole_moment",
                    contributions     = None,
                    predict_magnitude = True if self.is_dipole_moment_magnitude else False,
                    mean              = None,
                    stddev            = None,
                )
                output_modules.append(DIPOLE_MOMENT)

            print_function(f"Output_modules [{len(output_modules)}]: {output_modules}")

            self.model = AtomisticModel(representation, output_modules)
            print_function(f"Model parameters: {self.model}")

        if "cuda" in self.device.type:
            if len(self.gpu_info.get_gpu_in_use()) > 1: self.model = torch.nn.DataParallel(self.model, device_ids=self.gpu_info.get_gpu_in_use())
            elif self._force_gpu:
                if self._force_map is None: self.model = torch.nn.DataParallel(self.model)
                else:                       self.model = torch.nn.DataParallel(self.model, device_ids=self._force_map, output_device=self._force_map[0])
        print_function(f"{self.internal_name} [model building] done.")

    def build_trainer(self, weight:float = 1.0) -> None:

        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)

        # construct hooks # MeanSquaredError OR# RootMeanSquaredError
        metrics = [MeanAbsoluteError(p, p) if p != "forces" else MeanAbsoluteError(p, p, element_wise=True) for p in self.training_properties]

        hooks   = [
            CSVHook(log_path=self.model_path, metrics=metrics),
            ReduceLROnPlateauHook(optimizer, patience=15, factor=0.8, min_lr=1e-8, stop_after_min=True)
        ]

        # trainer
        loss_fun = self.loss_fun_builder(self.training_properties, loss_tradeoff=self.loss_tradeoff, weight=weight)
        self.trainer = Trainer(
            model_path        = self.model_path,
            model             = self.model,
            hooks             = hooks,
            loss_fn           = loss_fun,
            optimizer         = optimizer,
            train_loader      = self.train_loader,
            validation_loader = self.valid_loader,
        )

    def _train(self, epochs:int = None, indexes:str = None, xyz_file:str = None) -> None:
        print_function(f"{self.internal_name} Training...")
        if self.device.type == "cpu":  mess = f"{self.device}"
        if self.device.type == "cuda": mess = f"{self.device}: {self.gpu_info.get_gpu_in_use()}"

        for epoch in tqdm(range(epochs), f"Training [{mess}]", file=sys.stdout):
            epochs_done = self.storer.get(self.name4storer)

            if epoch <= epochs_done: continue
            else:
                _showed = False
                # Training
                self.trainer.train(device=self.device, n_epochs=1)

                # Storing checkpoint
                self.storer.put(what=epochs_done+1, name=self.name4storer)
                self.storer.dump()

                if epoch % self.validate_each_epoch == 0 and epoch != 0:
                    if not _showed: self.gpu_info.notify(True); _showed=True
                    self.validate()

                if epoch % self.predict_each_epoch == 0 and epoch != 0:
                    if not _showed: self.gpu_info.notify(True); _showed=True
                    if self.compare_with_foreign_model: self.predict(indexes=indexes, xyz_file=xyz_file, path2foreign_model=self.path2foreign_model)
                    self.predict(indexes=indexes, xyz_file=xyz_file)
                    self.use_model_on_test(db_name=self._get_db_name(xyz_file=xyz_file, indexes=indexes))


        print_function(f"{self.internal_name} [model training] done.")

    def train_model(self) -> None:
        """
        Main procedure of the training of neural network.

        """
        for xyz_file in self.nn_settings:
            print_function(f"XYZ data: {xyz_file}")
            #for indexes, epochs in self.nn_settings[xyz_file].items():
            for indexes, epochs, *w in self.nn_settings[xyz_file][self._index_epoch_weight_key[xyz_file]]:
                if len(w) == 0: w = self.nn_settings[xyz_file]['weight']
                print_function(f"Indexes: '{indexes}' | epochs: {epochs} | weight: {w}")

                self.prepare_databases(redo=False, index=indexes, xyz_file=xyz_file)
                db_name = self._get_db_name(xyz_file=xyz_file, indexes=indexes)
                self.prepare_train_valid_test_samples(db_name = db_name)

                if self.plot_enabled: self.visualize_interest_region(indexes=indexes, samples4showing=self.visualize_points_from_data, source_of_points=self.train_samples)

                # creating model instance: creating representation, output_modules for it
                self.build_model()
                self.print_info()
                # initial preparations
                if self._should_train: self.build_trainer(w)
                #
                self.name4storer = f"{self.network_name}_{db_name}.nn"
                if not self.storer.get(self.name4storer): self.storer.put(what=0, name=self.name4storer)
                print_function(f"--> [Storer]  epochs done: {self.storer.get(self.name4storer)}")
                if self._should_train: print_function(f"--> [Trainer] epochs done: {self.trainer.epoch}")

                #
                if self._should_train: self._train(epochs=epochs, indexes=indexes, xyz_file=xyz_file)
                # Show the last epoch
                self.gpu_info.notify(True)
                self.validate()
                self.predict(indexes=indexes, xyz_file=xyz_file)
                self.use_model_on_test(db_name=db_name)

                if self.downsample_threshold is not None:
                    self.downsample(indexes=indexes, xyz_file=xyz_file)
                #if epoch % self.downsample_each_epoch == 0 and epoch != 0:
                #    # downsample procedure
                #    self.downsample(indexes=indexes, xyz_file=xyz_file)

    def visualize_interest_region(self, indexes:str = None, samples4showing:int = 1, source_of_points:List[Atoms] = None, xyz_file:str = None) -> None:
        print_function(f"{self.internal_name} Visualizing regions of interest...")
        # visualization whole range of points
        if xyz_file:
            self.prepare_databases(redo=False, index=indexes, xyz_file=xyz_file)
            #db_name = f"{xyz_file}_{str(indexes)}_{self.units['ENERGY'].replace('/','')}_{self.units['FORCE'].replace('/','')}_{self.units['DIPOLE_MOMENT'].replace('/','')}.db"
            source_of_points = AtomsData(self.db_path + self._get_db_name(xyz_file=xyz_file, indexes=indexes), load_only=self.training_properties)
        # end
        num_samples = len(source_of_points)

        if samples4showing > num_samples:
            print_function(f"Warning! You requested samples for showing: {samples4showing}, however available only {num_samples}.")
            samples4showing = num_samples

        try:     start_region_of_interest, end_region_of_interest, step = [int(val) for val in indexes.split(":")]  # interval of interest
        except:
            try: start_region_of_interest, end_region_of_interest       = [int(val) for val in indexes.split(":")]  # interval of interest without step
            except: start_region_of_interest, end_region_of_interest    = 0, num_samples-1

        # choose number of points from the source_of_points of region of interest
        self.idx4vis = idx_samples = [int(i) for i in np.linspace(0, num_samples-1, samples4showing)]


        # for each training_prop
        for training_prop in self.training_properties:
            # not necessary
            if training_prop == "forces": continue
            print(f"Training prop: {training_prop}")
            samples2show = []

            for idx in idx_samples:
                _, props = source_of_points.get_properties(idx)
                samples2show.append(np.array(props[training_prop])) #

            y = np.array(samples2show)
            x = [int(i) for i in np.linspace(start_region_of_interest, end_region_of_interest, samples4showing)]
            assert(len(y) == len(x), "Strange it x-y lengths are different")
            if not self.using_matplotlib:
                key_name = "data: train/showed:["+str(num_samples)+"/"+str(samples4showing)+"] total:" + str(len(self.samples))

                # dipole moments
                if "dipole" in training_prop:
                    # dipole_moment_x, dipole_moment_y, dipole_moment_z
                    if y.shape[1] > 1:
                        for dim in range(y.shape[1]):
                            try: page = DM[dim]
                            except ValueError:
                                print(f"DM does not know the page for dim: {dim}. Aborting.")
                                sys.exit(1)
                            self.plotter_progress.plot(x=x, y=y[:,dim], key_name=key_name, page=page)
                    else:
                        ### dipole_moment_magnitude
                        self.plotter_progress.plot(x=x, y=y[:,0], key_name=key_name, page="dipole_moment_magnitude")
                else:
                    # energy
                    self.plotter_progress.plot(x=x, y=y[:,0],             key_name=key_name, page="xyz_file")
                    self.plotter_progress.plot(x=x, y=(y[:,0]-y[:,0][0]), key_name=key_name, page="xyz_file_sub")

    def downsample(self, indexes:str  = None, xyz_file:str = None) -> None:
        """
        Downsample method.

        Input:
        - indexes     [None] -- XX:XX:XX indexes for start / end / step
        - xyz_file    [None] -- path to xyz file
        """
        def compute_and_account(best_model, batch, idx):
            ## move batch to GPU, if necessary
            batch = {k: v.to(self.device) for k, v in batch.items()}
            number_atoms = len(batch['_atomic_numbers'][0])
            pred  = best_model(batch)

            if "energy"        in self.training_properties:
                preds["orig_energy"].append((idx, batch["energy"].detach().cpu().numpy() ))
                preds["pred_energy"].append((idx, pred["energy"].detach().cpu().numpy()) )
                # norm
                preds["orig_energy_norm"].append((idx, batch["energy"].detach().cpu().numpy()/number_atoms ))
                preds["pred_energy_norm"].append((idx, pred["energy"].detach().cpu().numpy() /number_atoms ))
            if "dipole_moment" in self.training_properties:
                preds["orig_dipole_moment"].append((idx, batch["dipole_moment"].detach().cpu().numpy()))
                preds["pred_dipole_moment"].append((idx,  pred["dipole_moment"].detach().cpu().numpy()))
            if "dipole_moment_magnitude" in self.training_properties:
                preds["orig_dipole_moment"].append((idx, batch["dipole_moment_magnitude"].detach().cpu().numpy()))
                preds["pred_dipole_moment"].append((idx,  pred["dipole_moment_magnitude"].detach().cpu().numpy()))

        network_name = key_prefix = str(self.network_name)
        model_path   = os.path.join(self.model_path, 'best_model')
        epochs_done  = self.storer.get(self.name4storer)

        # creating folder for model test
        print_function(f"{self.internal_name} Downsampling based on [{network_name}]...")

        test_path = os.path.join(self.test_path, network_name); os.makedirs(test_path, exist_ok=True)

        #check_xyz_file = list(self.check_list_files.keys()) + [xyz_file]
        check_xyz_file = [xyz_file]  # Do we need downsampling on check_list files? Currently the answer is no

        for xyz_file in check_xyz_file:
            print_function(f"Reading {xyz_file}...")
            self.prepare_databases(redo=False, index=":", xyz_file=xyz_file)
            #db_name = f"{xyz_file}_{str(indexes)}_{self.units['ENERGY'].replace('/','')}_{self.units['FORCE'].replace('/','')}_{self.units['DIPOLE_MOMENT'].replace('/','')}.db"
            db_path_fname = os.path.join(self.db_path, self._get_db_name(xyz_file=xyz_file, indexes=indexes))
            print_function(f"Loading... | {db_path_fname}")
            #
            #self.SUBSAMPLES_LOADER = subsamples_loader_train = AtomsLoader(self.train_samples, batch_size=1)
            self.SUBSAMPLES_LOADER = subsamples_loader = AtomsLoader(self.samples, batch_size=1)
            #subsamples_loader_valid = AtomsLoader(self.valid_samples, batch_size=1)
            #subsamples_loader_test = AtomsLoader(self.test_samples, batch_size=1)
            #idxs = self.idx4vis  # idx for downsample self.idx4vis -- visualization
            idxs = len(subsamples_loader)  # idx for downsample self.idx4vis -- visualization

            #if xyz_file in self.db_epochs.keys():
            #    self.SUBSAMPLES_LOADER = subsamples_loader = AtomsLoader(self.train_samples, batch_size=1)
            #    idxs = self.idx4vis  # idx for downsample self.idx4vis -- visualization
            #    #trained_subset = True
            # check_list file
            #else:
            #    samples = AtomsData(db_path_fname, load_only=self.training_properties)  # pick the db
            #    subsamples, idxs = pack.get_subset(
            #        data         = samples,
            #        num_samples  = self.check_list_files[xyz_file]['num_points'], #self.visualize_points_from_nn,
            #    )
            #    subsamples_loader = AtomsLoader(subsamples, batch_size=1)
            #    trained_subset = False
            #    # use model on test
            #    self.use_model_on_test(_subsamples_loader = subsamples_loader, need2plot=False)

            print_function(f"[{network_name}] Loading the last best model")
            best_model = pack.utils.load_model(model_path, map_location=self.device)

            print_function(f"[Downsampling] Predicting on subset [#{len(subsamples_loader)}]...")
            self.preds = preds = defaultdict(list)

            #if not trained_subset: #len(subsamples_loader) == self.visualize_points_from_nn:
            #    for idx, batch in enumerate(tqdm(subsamples_loader, f"Predicting [{self.device}]")): compute_and_account(best_model, batch, idxs[idx])
            #else:
            #    for idx, batch in enumerate(tqdm(subsamples_loader, f"Predicting [{self.device}]")):
            #        if idx in idxs: compute_and_account(best_model, batch, idx)

            for idx, batch in enumerate(tqdm(subsamples_loader, f"[Downsampling] Predicting [{self.device}]")):
                #if idx in idxs: compute_and_account(best_model, batch, idx)
                compute_and_account(best_model, batch, idx)

            if 'energy' in self.training_properties:
                pred_energy        = np.array(preds["pred_energy"], dtype=np.float64)
                sorted_pred_energy = pred_energy[pred_energy[:,0].argsort()]
                orig_energy        = np.array(preds["orig_energy"], dtype=np.float64)
                sorted_orig_energy = orig_energy[orig_energy[:,0].argsort()]
                ##
                #pred_energy = np.array(preds["pred_energy"], dtype=[('idx','i8'),('val', 'f8')])
                #orig_energy = np.array(preds["orig_energy"], dtype=[('idx','i8'),('val', 'f8')])

                #samples_to_account = len(orig_energy)
                #energy_error = np.sum( np.abs(pred_energy['val'] - orig_energy['val']) ) / samples_to_account
                ##

                #
                delta_energy = np.array(orig_energy, copy=True) # Copy array
                delta_energy[:,1] = pred_energy[:,1] - orig_energy[:,1]  # Pred - Orig
                #
                self.OUTSIDE = outside = delta_energy[ abs(delta_energy[:,1]) > self.downsample_threshold]  # idx, energy
                self.INSIDE  = inside  = delta_energy[ abs(delta_energy[:,1]) < self.downsample_threshold]  # idx, energy
                # # # TEMPORARLY
                #self.preds_copy =  copy.deepcopy(self.preds)

                # CHECK LOSS
                pred_energy = np.array(self.preds["pred_energy"], dtype=[('idx','i8'),('val', 'f8')])
                orig_energy = np.array(self.preds["orig_energy"], dtype=[('idx','i8'),('val', 'f8')])

                samples_to_account = len(orig_energy)
                energy_error = np.sum( np.abs(pred_energy['val'] - orig_energy['val']) ) / samples_to_account

                print("Energy LOSS: ", energy_error)

                # REDUCED ARRAY
                self.preds.clear()
                for idx, batch in enumerate(tqdm(subsamples_loader, f"[Downsampling] Predicting [{self.device}]")):
                    if idx in inside[:,0]: compute_and_account(best_model, batch, idx)

                #pred_energy_new        = np.array(self.preds["pred_energy"], dtype=np.float64)
                #sorted_pred_energy_new = pred_energy[pred_energy[:,0].argsort()]
                #orig_energy_new        = np.array(self.preds["orig_energy"], dtype=np.float64)
                #sorted_orig_energy_new = orig_energy[orig_energy[:,0].argsort()]

                # CHECK LOSS
                pred_energy = np.array(self.preds["pred_energy"], dtype=[('idx','i8'),('val', 'f8')])
                orig_energy = np.array(self.preds["orig_energy"], dtype=[('idx','i8'),('val', 'f8')])

                samples_to_account = len(orig_energy)
                energy_error = np.sum( np.abs(pred_energy['val'] - orig_energy['val']) ) / samples_to_account

                print("REDUCED Energy LOSS: ", energy_error)

                # saving outside and inside samples

                inside_len  = len(inside[:,0])
                outside_len = len(outside[:,0])

                # TODO: Forces, dipole_moment? internal_energy -> energy

                for idx, batch in enumerate(tqdm(subsamples_loader, f"[Downsampling] Saving inside [{self.device}]")):
                    if idx in inside[:,0]:
                        positions = batch['_positions'].squeeze()
                        _number_of_atoms = positions.shape[0] #
                        a = Atoms(symbols="C"+str(_number_of_atoms), positions=positions)
                        if "energy" in batch.keys(): a.set_internal_potential_energy(batch['energy'].squeeze().item())
                        if "forces" in batch.keys(): a.set_internal_forces(batch['forces'].squeeze().numpy())
                        if "dipole_moment" in batch.keys(): a.set_internal_dipole_moment(batch['dipole_moment'].squeeze())

                        write(filename=f"{self.xyz_path}/inside_model{self.network_name}_threshold{self.downsample_threshold}_{str(inside_len)}.extxyz", images=a, format="extxyz", append=True)

                for idx, batch in enumerate(tqdm(subsamples_loader, f"[Downsampling] Saving outside [{self.device}]")):
                    if idx in outside[:,0]:
                        positions = batch['_positions'].squeeze()
                        _number_of_atoms = positions.shape[0] #
                        a = Atoms(symbols="C"+str(_number_of_atoms), positions=positions)
                        if "energy" in batch.keys(): a.set_internal_potential_energy(batch['energy'].squeeze().item())
                        if "forces" in batch.keys(): a.set_internal_forces(batch['forces'].squeeze().numpy())
                        if "dipole_moment" in batch.keys(): a.set_internal_dipole_moment(batch['dipole_moment'].squeeze())
                        write(filename=f"{self.xyz_path}/outside_model{self.network_name}_threshold{self.downsample_threshold}_{str(outside_len)}.extxyz", images=a, format="extxyz", append=True)

                # plot mean and std inside
                try:    sysname = xyz_file.replace("_", " ")
                except: sysname = "Downsampled data"
                _idx, _energy = inside[:, 0], inside[:, 1]
                _mean = np.mean(_energy)
                _std  = np.std(_energy, ddof=1)
                key_name = f"{key_prefix.replace('_', '')} on {sysname}: epochs:{str(epochs_done)} | predicted: {str(len(_idx))}" # TODO energy_error to smth better...
                self.plotter_progress.plot(page="energy_loss_per_sample_inside", key_name=f"mean{_mean:.5f} | std:{_std:.5f} energy loss: {energy_error}", plotLine=False,
                                           x=_idx, y= list(zip(
                                               [_mean for _ in range(len(_idx))],
                                               [_std  for _ in range(len(_idx))])),
                                           errorStyle="fillvert",
                                           )
                self.plotter_progress.plot(page="energy_loss_per_sample_inside", key_name=key_name, plotLine=False,
                                           x=_idx, y= _energy)



    def predict(self, indexes:str  = None, xyz_file:str = None, path2foreign_model:str = None, need2plot:bool = True) -> None:
        """
        Prediction method.

        Input:
        - indexes     [None] -- XX:XX:XX indexes for start / end / step
        - xyz_file    [None] -- path to xyz file
        - path2foreign_model [None]  -- if set used for comparing
        """
        if self.meta:
            """
            * No need to predict anything on the remote job
            """
            return
        else:
            def compute_and_account(best_model, batch, idx):
                ## move batch to GPU, if necessary
                batch = {k: v.to(self.device) for k, v in batch.items()}
                number_atoms = len(batch['_atomic_numbers'][0])
                pred  = best_model(batch)

                if "energy"        in self.training_properties:
                    preds["orig_energy"].append((idx, batch["energy"].detach().cpu().numpy() ))
                    preds["pred_energy"].append((idx, pred["energy"].detach().cpu().numpy()) )
                    # norm
                    orig_energy_norm = batch["energy"].detach().cpu().numpy()/number_atoms
                    pred_energy_norm = pred["energy"].detach().cpu().numpy()/number_atoms
                    preds["orig_energy_norm"].append((idx, orig_energy_norm))
                    preds["pred_energy_norm"].append((idx, pred_energy_norm))
                if "dipole_moment" in self.training_properties:
                    preds["orig_dipole_moment"].append((idx, batch["dipole_moment"].detach().cpu().numpy()))
                    preds["pred_dipole_moment"].append((idx,  pred["dipole_moment"].detach().cpu().numpy()))
                if "dipole_moment_magnitude" in self.training_properties:
                    preds["orig_dipole_moment"].append((idx, batch["dipole_moment_magnitude"].detach().cpu().numpy()))
                    preds["pred_dipole_moment"].append((idx,  pred["dipole_moment_magnitude"].detach().cpu().numpy()))

            if path2foreign_model is not None:
                if not self.foreign_plotted: self.foreign_plotted = True
                network_name = key_prefix = "foreign model"
                model_path   = os.path.join(path2foreign_model, 'best_model')
                #fname_name   = "before_energy_predicted_"+str(indexes)+".dat"
                epochs_done  = "[UNKNOWN]"
            else:
                network_name = key_prefix = str(self.network_name)
                model_path   = os.path.join(self.model_path, 'best_model')
                epochs_done  = self.storer.get(self.name4storer)
                #fname_name   = "before_energy_predicted_"+str(indexes)+"_epochs"+str(epochs_done)+"_each"+str(self.visualize_each_point_from_nn)+"sample.dat"

            # creating folder for model test
            print_function(f"{self.internal_name} Prediction check [{network_name}]")

            test_path = os.path.join(self.test_path, network_name); os.makedirs(test_path, exist_ok=True)
            #fname     = os.path.join(test_path, fname_name)

            check_xyz_file = list(self.check_list_files.keys()) + [xyz_file]

            for xyz_file in check_xyz_file:
                #
                print_function(f"Reading {xyz_file}...")
                self.prepare_databases(redo=False, index=":", xyz_file=xyz_file)
                #db_name = f"{xyz_file}_{str(indexes)}_{self.units['ENERGY'].replace('/','')}_{self.units['FORCE'].replace('/','')}_{self.units['DIPOLE_MOMENT'].replace('/','')}.db"
                db_path_fname = os.path.join(self.db_path, self._get_db_name(xyz_file=xyz_file, indexes=indexes))
                print_function(f"Loading... | {db_path_fname}")
                #
                if xyz_file in self.nn_settings.keys():
                    subsamples_loader = AtomsLoader(self.train_samples, batch_size=1)
                    idxs = self.idx4vis
                    trained_subset = True
                else:
                    samples = AtomsData(db_path_fname, load_only=self.training_properties)  # pick the db
                    subsamples, idxs = pack.get_subset(
                        data         = samples,
                        num_samples  = self.check_list_files[xyz_file]['num_points'], #self.visualize_points_from_nn,
                    )
                    subsamples_loader = AtomsLoader(subsamples, batch_size=1)
                    trained_subset = False
                    # use model on test
                    self.use_model_on_test(_subsamples_loader = subsamples_loader, need2plot=False)

                print_function(f"[{network_name}] Loading the last best model")
                best_model = pack.utils.load_model(model_path, map_location=self.device)

                print_function(f"Predicting on subset [#{len(idxs)}]...")
                self.preds = preds = defaultdict(list)

                if not trained_subset: #len(subsamples_loader) == self.visualize_points_from_nn:
                    for idx, batch in enumerate(tqdm(subsamples_loader, f"Predicting [{self.device}]")): compute_and_account(best_model, batch, idxs[idx])
                else:
                    for idx, batch in enumerate(tqdm(subsamples_loader, f"Predicting [{self.device}]")):
                        if idx in idxs: compute_and_account(best_model, batch, idx)

                ## Plotting
                if (self.plot_enabled and not self.using_matplotlib) and need2plot:
                    try: sysname = xyz_file.replace("_", " ")
                    except:
                        if not trained_subset: sysname = "unnamed"
                        else: sysname = "data"

                    if 'energy' in self.training_properties:
                        pred_energy        = np.array(preds["pred_energy"], dtype=np.float64)
                        sorted_pred_energy = pred_energy[pred_energy[:,0].argsort()]
                        orig_energy        = np.array(preds["orig_energy"], dtype=np.float64)
                        sorted_orig_energy = orig_energy[orig_energy[:,0].argsort()]
                        # norm
                        pred_energy_norm        = np.array(preds["pred_energy_norm"], dtype=np.float64)
                        sorted_pred_energy_norm = pred_energy_norm[pred_energy_norm[:,0].argsort()]
                        orig_energy_norm        = np.array(preds["orig_energy_norm"], dtype=np.float64)
                        sorted_orig_energy_norm = orig_energy_norm[orig_energy_norm[:,0].argsort()]

                        if trained_subset: key_name = f"{key_prefix.replace('_', '')} on {sysname}: epochs:{str(epochs_done)} | predicted: {str(len(pred_energy))}"
                        else:              key_name = f"{key_prefix.replace('_', '')} on {sysname}: epochs:{str(epochs_done)} | predicted: {str(len(pred_energy))}"
                        self.plotter_progress.plot(page="xyz_file",     key_name = key_name,
                                                   x=sorted_pred_energy[:,0], y=sorted_pred_energy[:,1],  animation=True)
                        self.plotter_progress.plot(page="xyz_file_sub", key_name = key_name,
                                                   x=sorted_pred_energy[:,0], y=(sorted_pred_energy[:,1] - sorted_pred_energy[:,1][0]), )
                        #self.plotter_progress.plot(page="delta_energy", key_name = key_name,
                        #                           x=sorted_pred_energy[:,0], y=(sorted_pred_energy[:,1] - sorted_orig_energy[:,1]),)

                        _energy_loss_per_sample = sorted_pred_energy[:,1] - sorted_orig_energy[:,1]
                        sorted_pred_energy[:, 0]
                        # plot mean and std
                        _mean = np.mean(_energy_loss_per_sample)
                        _std  = np.std(_energy_loss_per_sample, ddof=1)
                        self.plotter_progress.plot(page="energy_loss_per_sample", key_name=f"mean{_mean:.5f}| std:{_std:.5f}", plotLine=False,
                                                   x=sorted_pred_energy[:,0], y= list(zip(
                                                       [_mean for _ in range(len(sorted_pred_energy[:,0]))],
                                                       [_std  for _ in range(len(sorted_pred_energy[:,0]))])),
                                                   errorStyle="fillvert",
                                                   )
                        self.plotter_progress.plot(page="energy_loss_per_sample", key_name = key_name,
                                                   x=sorted_pred_energy[:,0], y=_energy_loss_per_sample,)

                        self.plotter_progress.plot(page="diag_energy", key_name = key_name, plotLine=False,
                                                   x=sorted_orig_energy[:, 1], y=sorted_pred_energy[:,1])
                        self.plotter_progress.plot(page="diag_energy_norm", key_name = key_name, plotLine=False,
                                                   x=sorted_orig_energy_norm[:, 1], y=sorted_pred_energy_norm[:,1])

                    if 'dipole_moment_magnitude' in self.training_properties:
                        pred_dipole_moment        = np.array(preds["pred_dipole_moment"], dtype=np.float64)
                        sorted_pred_dipole_moment = pred_dipole_moment[pred_dipole_moment[:,0].argsort()]
                        orig_dipole_moment        = np.array(preds["orig_dipole_moment"], dtype=np.float64)
                        sorted_orig_dipole_moment = orig_dipole_moment[orig_dipole_moment[:,0].argsort()]

                        if trained_subset: key_name = f"{sysname} data: train/showed:["+str(len(self.train_samples))+"/"+str(len(idxs))+"] total:" + str(len(self.samples))
                        else:              key_name = f"{sysname} data: train/showed:[0/"+str(len(idxs))+"] total:" + str(len(samples))

                        # original
                        self.plotter_progress.plot(page="dipole_moment_magnitude", key_name=key_name,
                                                   x=sorted_orig_dipole_moment[:,0],
                                                   y=sorted_orig_dipole_moment[:,1])

                        self.plotter_progress.plot(page="delta_dipole_moment_magnitude", key_name=key_name,
                                                   x=sorted_pred_dipole_moment[:,0],
                                                   y=(sorted_pred_dipole_moment[:,1]-sorted_orig_dipole_moment[:,1]))

                        self.plotter_progress.plot(page="diag_dp_magnitude", key_name = key_name, plotLine=False,
                                                   x=sorted_orig_dipole_moment[:,1],
                                                   y=sorted_pred_dipole_moment[:,1])

                    if 'dipole_moment' in self.training_properties:
                        # not a magnitude --> [x, y ,z]
                        pred_dipole_moment        = np.array(preds["pred_dipole_moment"], dtype=[('idx', 'i8'), ('xyz', 'f8', (1, 3))])
                        sorted_pred_dipole_moment = pred_dipole_moment[pred_dipole_moment["idx"].argsort()]
                        orig_dipole_moment        = np.array(preds["orig_dipole_moment"], dtype=[('idx', 'i8'), ('xyz', 'f8', (1, 3))])
                        sorted_orig_dipole_moment = orig_dipole_moment[orig_dipole_moment["idx"].argsort()]

                        # original --> [x,y,z]
                        if trained_subset: key_name = f"{sysname} data: train/showed:["+str(len(self.train_samples))+"/"+str(len(idxs))+"] total:" + str(len(self.samples))
                        else:              key_name = f"{sysname} data: train/showed:[0/"+str(len(idxs))+"] total:" + str(len(samples))
                        self.plotter_progress.plot(page="dipole_moment_x", key_name=key_name,
                                                   x=sorted_orig_dipole_moment["idx"], y=np.concatenate(sorted_orig_dipole_moment["xyz"][...,0]))
                        self.plotter_progress.plot(page="dipole_moment_y", key_name=key_name,
                                                   x=sorted_orig_dipole_moment["idx"], y=np.concatenate(sorted_orig_dipole_moment["xyz"][...,1]))
                        self.plotter_progress.plot(page="dipole_moment_z", key_name=key_name,
                                                   x=sorted_orig_dipole_moment["idx"], y=np.concatenate(sorted_orig_dipole_moment["xyz"][...,2]))

                        #
                        #key_name = f"{key_prefix} {sysname}: epochs:{str(epochs_done)} | predicted: {str(len(pred_dipole_moment))}"
                        if trained_subset: key_name = f"{key_prefix.replace('_', '')} on {sysname}: epochs:{str(epochs_done)} | predicted: {str(len(sorted_orig_dipole_moment['idx']))}"
                        else:              key_name = f"{key_prefix.replace('_', '')} on {sysname}: epochs:{str(epochs_done)} | predicted: {str(len(sorted_orig_dipole_moment['idx']))}"
                        self.plotter_progress.plot(page="dipole_moment_x", key_name=key_name,
                                                   x=sorted_pred_dipole_moment["idx"],
                                                   y=np.concatenate(sorted_pred_dipole_moment["xyz"][...,0]))
                        self.plotter_progress.plot(page="dipole_moment_y", key_name=key_name,
                                                   x=sorted_pred_dipole_moment["idx"],
                                                   y=np.concatenate(sorted_pred_dipole_moment["xyz"][...,1]))
                        self.plotter_progress.plot(page="dipole_moment_z", key_name=key_name,
                                                   x=sorted_pred_dipole_moment["idx"],
                                                   y=np.concatenate(sorted_pred_dipole_moment["xyz"][...,2]))

                        # delta  --> [x,y,z]
                        self.plotter_progress.plot(page="delta_dipole_moment_x", key_name=key_name,
                                                   x=sorted_pred_dipole_moment["idx"],
                                                   y=(np.concatenate(sorted_pred_dipole_moment["xyz"][...,0])-np.concatenate(sorted_orig_dipole_moment["xyz"][...,0])) )
                        self.plotter_progress.plot(page="delta_dipole_moment_y", key_name=key_name,
                                                   x=sorted_pred_dipole_moment["idx"],
                                                   y=(np.concatenate(sorted_pred_dipole_moment["xyz"][...,1])-np.concatenate(sorted_orig_dipole_moment["xyz"][...,1])) )
                        self.plotter_progress.plot(page="delta_dipole_moment_z", key_name=key_name,
                                                   x=sorted_pred_dipole_moment["idx"],
                                                   y=(np.concatenate(sorted_pred_dipole_moment["xyz"][...,2])-np.concatenate(sorted_orig_dipole_moment["xyz"][...,2])) )

                        # diag --> [x,y,z]
                        self.plotter_progress.plot(page="diag_dp_x", key_name = key_name, plotLine=False,
                                                   x=np.concatenate(sorted_orig_dipole_moment["xyz"][...,0]),
                                                   y=np.concatenate(sorted_pred_dipole_moment["xyz"][...,0]))
                        self.plotter_progress.plot(page="diag_dp_y", key_name = key_name, plotLine=False,
                                                   x=np.concatenate(sorted_orig_dipole_moment["xyz"][...,1]),
                                                   y=np.concatenate(sorted_pred_dipole_moment["xyz"][...,1]))
                        self.plotter_progress.plot(page="diag_dp_z", key_name = key_name, plotLine=False,
                                                   x=np.concatenate(sorted_orig_dipole_moment["xyz"][...,2]),
                                                   y=np.concatenate(sorted_pred_dipole_moment["xyz"][...,2]))


    def use_model_on_test(self, db_name:str = None, path2model:str = None, _subsamples_loader:AtomsLoader = None, need2plot:bool = True) -> None:
        """
        The function provides ability to use model [trained/foreign] on the test data and plot results (if necessary (need2plot flag))

        """

        def compute_and_account(best_model, batch, idx):
            ## move batch to GPU, if necessary
            batch = {k: v.to(self.device) for k, v in batch.items()}
            pred = best_model(batch)
            if "energy"        in self.training_properties:
                preds["orig_energy"].append((idx, batch["energy"].detach().cpu().numpy() ))
                preds["pred_energy"].append((idx, pred["energy"].detach().cpu().numpy()) )
                # forces
                preds["orig_forces"].append((idx, batch["forces"].detach().cpu().numpy() ))
                preds["pred_forces"].append((idx, pred["forces"].detach().cpu().numpy()) )
            if "dipole_moment" in self.training_properties:
                preds["orig_dipole_moment"].append((idx, batch["dipole_moment"].detach().cpu().numpy()))
                preds["pred_dipole_moment"].append((idx,  pred["dipole_moment"].detach().cpu().numpy()))
            if "dipole_moment_magnitude" in self.training_properties:
                preds["orig_dipole_moment"].append((idx, batch["dipole_moment_magnitude"].detach().cpu().numpy()))
                preds["pred_dipole_moment"].append((idx,  pred["dipole_moment_magnitude"].detach().cpu().numpy()))

        which = "trained" if path2model is None else "[FOREIGN]"
        if path2model is None: best_model = self.model
        else:                  best_model = pack.utils.load_model(self.model_path + "/best_model", map_location=self.device)

        print_function(f"{self.internal_name} Using the {which} model on the test data...")

        energy_error, forces_error, = torch.Tensor(np.array([0.])), torch.tensor(np.array([0., 0., 0.]))
        if self.is_dipole_moment_magnitude: dipole_moment_error = torch.Tensor(np.array([0.]))
        else:                               dipole_moment_error = torch.tensor(np.array([0., 0., 0.]))

        if self.test_loader is None: self.prepare_train_valid_test_samples(db_name=db_name)

        if _subsamples_loader is not None: subsamples_loader = _subsamples_loader
        else:                              subsamples_loader = AtomsLoader(self.test_samples, batch_size=1)

        self.test_preds = preds = defaultdict(list)

        for idx, batch in enumerate(tqdm(subsamples_loader, f"{self.network_name} on test dataset [{self.device}]")): compute_and_account(best_model, batch, idx)

        # need to calculate loss
        if 'energy' in self.training_properties:
            pred_energy = np.array(preds["pred_energy"], dtype=[('idx','i8'),('val', 'f8')])
            orig_energy = np.array(preds["orig_energy"], dtype=[('idx','i8'),('val', 'f8')])

            samples_to_account = len(orig_energy)
            energy_error = np.sum( np.abs(pred_energy['val'] - orig_energy['val']) ) / samples_to_account

            # and force
            # --> structure:
            #                 [idx, array(X,...,X)]
            #                            ...
            #                 [idx, array(X,...,X)] <-- second element is np.array

            # checking if an array is heterogeneous
            heterogeneous_array = False
            fi = preds['pred_forces'][0][1].shape[1]  # second item of the shape
            for item in preds['pred_forces']:
                if fi != item[1].shape[1]: heterogeneous_array = True

            if heterogeneous_array:
                nparrs_list: List[np.array] = []
                for idx, _ in enumerate(preds['pred_forces']):
                    # [mean_over_X, mean_over_Y, mean_over_Z] <-- list of this
                    nparrs_list.append( np.mean( np.abs(preds['pred_forces'][idx][1] - preds['orig_forces'][idx][1])[0], axis=(0,) ) )
                forces_error = torch.Tensor( np.mean(nparrs_list, axis=(0,)) )
            else:
                # <Warning> In heterogeneous arrays this trick does not work!
                row_size    = preds['pred_forces'][0][1].shape[1]  # 1 --> second dim
                pred_forces = np.array(preds["pred_forces"], dtype=[('idx', 'i8'), ('xyz', 'f8', (row_size, 3))])
                orig_forces = np.array(preds["orig_forces"], dtype=[('idx', 'i8'), ('xyz', 'f8', (row_size, 3))])
                forces_error = torch.Tensor ( np.mean ( np.mean( np.abs(pred_forces['xyz'] - orig_forces['xyz']), axis=(0,) ), axis=(0,) ) )

        if "dipole_moment" in self.training_properties:
            pred_dipole_moment        = np.array(preds["pred_dipole_moment"], dtype=[('idx', 'i8'), ('xyz', 'f8', (1, 3))])
            orig_dipole_moment        = np.array(preds["orig_dipole_moment"], dtype=[('idx', 'i8'), ('xyz', 'f8', (1, 3))])

            # np.array:[[<axis_mean_x>, <axis_mean_y>, <axis_mean_z>]]
            dipole_moment_error = torch.Tensor( np.mean(np.abs(pred_dipole_moment['xyz'] - orig_dipole_moment['xyz']), axis=(0,))[0]) # take internal array [[internal]]
            samples_to_account = len(orig_dipole_moment)

        if "dipole_moment_magnitude" in self.training_properties:
            pred_dipole_moment        = np.array(preds["pred_dipole_moment"], dtype=np.float64)
            orig_dipole_moment        = np.array(preds["orig_dipole_moment"], dtype=np.float64)

            # np.array: <axis_mean>
            dipole_moment_error = torch.Tensor([np.mean(np.abs(pred_dipole_moment[:,1] - orig_dipole_moment[:,1]), axis=(0,))]) # Tensor[internal]
            samples_to_account = len(orig_dipole_moment)

        # TODO: 24?
        print_function(f"""

Test LOSS | epochs {self.storer.get(self.name4storer)} | samples into account: #{samples_to_account}:
          <energy> [{self.units["ENERGY"]}]: {str(energy_error):>24}
          <forces> [{self.units["FORCE"]}]: {str(forces_error):>25}
          <dipole moment> [{self.units["DIPOLE_MOMENT"]}]: {str(dipole_moment_error):>25}

        """)

        # Plotting
        if (self.plot_enabled and not self.using_matplotlib) and need2plot:
            network_name = key_prefix = str(self.network_name)
            epochs_done  = self.storer.get(self.name4storer)
            key_name = f"{key_prefix.replace('_','')} on test dataset: epochs:{str(epochs_done)} | predicted:"

            if "energy" in self.training_properties:
                # energy
                pred_energy        = np.array(preds["pred_energy"], dtype=np.float64)
                sorted_pred_energy = pred_energy[pred_energy[:,0].argsort()]
                orig_energy        = np.array(preds["orig_energy"], dtype=np.float64)
                sorted_orig_energy = orig_energy[orig_energy[:,0].argsort()]

                key_name += f"{len(pred_energy)}"

                self.plotter_progress.plot(page="diag_energy", key_name = key_name, plotLine=False,
                                           x=sorted_orig_energy[:, 1], y=sorted_pred_energy[:,1])

            if "dipole_moment" in self.training_properties:
                pred_dipole_moment        = np.array(preds["pred_dipole_moment"], dtype=[('idx', 'i8'), ('xyz', 'f8', (1, 3))])
                sorted_pred_dipole_moment = pred_dipole_moment[pred_dipole_moment["idx"].argsort()]
                orig_dipole_moment        = np.array(preds["orig_dipole_moment"], dtype=[('idx', 'i8'), ('xyz', 'f8', (1, 3))])
                sorted_orig_dipole_moment = orig_dipole_moment[orig_dipole_moment["idx"].argsort()]
                # diag
                key_name += f"{len(pred_dipole_moment)}"
                self.plotter_progress.plot(page="diag_dp_x", key_name = key_name, plotLine=False,
                                           x=np.concatenate(sorted_orig_dipole_moment["xyz"][...,0]),
                                           y=np.concatenate(sorted_pred_dipole_moment["xyz"][...,0]))
                self.plotter_progress.plot(page="diag_dp_y", key_name = key_name, plotLine=False,
                                           x=np.concatenate(sorted_orig_dipole_moment["xyz"][...,1]),
                                           y=np.concatenate(sorted_pred_dipole_moment["xyz"][...,1]))
                self.plotter_progress.plot(page="diag_dp_z", key_name = key_name, plotLine=False,
                                           x=np.concatenate(sorted_orig_dipole_moment["xyz"][...,2]),
                                           y=np.concatenate(sorted_pred_dipole_moment["xyz"][...,2]))

            if "dipole_moment_magnitude" in self.training_properties:
                pred_dipole_moment        = np.array(preds["pred_dipole_moment"], dtype=np.float64)
                sorted_pred_dipole_moment = pred_dipole_moment[pred_dipole_moment[:,0].argsort()]
                orig_dipole_moment        = np.array(preds["orig_dipole_moment"], dtype=np.float64)
                sorted_orig_dipole_moment = orig_dipole_moment[orig_dipole_moment[:,0].argsort()]
                # diag
                key_name += f"{len(pred_dipole_moment)}"
                self.plotter_progress.plot(page="diag_dp_magnitude", key_name = key_name, plotLine=False,
                                           x=sorted_orig_dipole_moment[:,1],
                                           y=sorted_pred_dipole_moment[:,1])

    def prepare_network(self, redo:bool = False) -> None:
        self.create_model_path(redo=redo)
        self.gpu_info.notify()
        self.train_model()

