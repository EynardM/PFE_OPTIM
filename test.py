from util.imports import *
from util.locations import *
from util.helpers import *
from util.objects import *
from util.datamodule import get_data

from algorithms.helpers import *
from algorithms.run import *

journey1 = Journey(starting_time=datetime(2024, 2, 10, 8, 0), ending_time=datetime(2024, 2, 10, 12, 0))
journey2 = Journey(starting_time=datetime(2024, 2, 10, 8, 0), ending_time=datetime(2024, 2, 10, 12, 0))
print(journey1 == journey2)