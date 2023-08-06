# NNmeta

NNmeta is created in order to use [NNPackage](https://github.com/AlexanderDKazakov/schnetpack). 

## Installation

### Install with pip [PyPi]:

```
pip3 install nnmeta
```

### Install from source

#### Clone the repository

```
git clone https://github.com/AlexanderDKazakov/nnmeta
cd nnmeta
```

#### Install requirements

```
pip3 install -r requirements.txt
```

#### Install NNmeta

```
pip3 install .
```

## Usage

NNmeta support certain convention in data structure and it is required to structure the data in such way:

```
# /path/to/my/base

base
└── xyz
    ├── samples.xyz
    └── samples_for_cc.xyz
```

After first run additional folders will be created: `models`, `dbs`, `splits`, `tests`

```python3
from nnmeta import NNClass # this is a main class for NN training 

info = dict(
	runner = {  # network name
		# data source [extended xyz file]; used for converting to DB [internal usage]
		# "filename" : {"range" ex. [from:to:step], epochs should be done}
		"samples.xyz" : {":" : 20},  # train `runner` nn on all samples of `samples.xyz` 20 epochs
	},
	
	runner_features = dict(
		n_features              = 64,    # details in NN class [default is 128]
		n_filters               = 32,    #
		n_gaussians             = 12,    # default 25
		batch_size              = 512,   #                     [parameter for tuning]
		lr                      = 1e-4,  # learning rate       [parameter for tuning]
		db_properties           = ("energy", "forces", "dipole_moment"), # what can be found in the `samples.xyz` file
		training_properties     = ("energy", "forces", "dipole_moment"), # what one wants to train
		loss_tradeoff           = (0.2, 0.8, 0.6),
		n_layers_energy_force   = 2,     # default 2           [parameter for tuning]
		n_neurons_energy_force  = None,  # default None        [parameter for tuning]
		n_layers_dipole_moment  = 2,     # default 2           [parameter for tuning]
		n_neurons_dipole_moment = None,  # default None        [parameter for tuning]
		loss_function_choice    = "mse", # "mae", "mse", "sae"
		
		train_samples_percent              = 70,
		valid_samples_percent              = 20,
		
		predict_each_epoch                 = 200,
		validate_each_epoch                = 30,
       
   		# cross-check with next files
       		check_list_files = {
		# this file should lie in the same `xyz` dir
			"samples_for_cc.xyz" : dict(num_points = 1000),
       		}
	)
)

nn = NNClass(info=info, network_name="runner", 
			system_path="/path/to/my/base")
nn.prepare_network()

```

## Contribution

Feel free to contribute to the project, but please create initially an issue with detailed problem and way to resolve it. 

## License

MIT
