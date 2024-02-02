from util.imports import * 
from util.objects import *
from util.locations import *
from util.helpers import *
from util.datamodule import get_data

# Getting the data
measurements, tanks, makers = get_data()

# Getting parameters
optimization_parameters, storehouse, agent = parse_config('config.json')
