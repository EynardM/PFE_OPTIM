from util.imports import *
from util.locations import *
from util.helpers import *
from util.objects import *
from optim.helpers import *

def permutation(journey: Journey, tanks: List[Tank], optimization_parameters: OptimizationParameters):
    # Get unused tanks
    unused_tanks = get_unused_tanks(journey=journey, tanks=tanks)

    # Select an unused tank 
    tank_chosen = random.choice(unused_tanks)

    # Get the available positions to put the tank
    cycles_positions = get_available_cycles_positions(journey=journey, choice=tank_chosen, optimization_parameters=optimization_parameters)
    colored(cycles_positions, "red")

    # Choose an available pair of cycle/position
    cycle_index, cycle_position = get_random_position(cycles_positions)
    colored(cycle_index, "cyan")
    colored(cycle_position, "cyan")