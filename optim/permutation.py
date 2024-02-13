from util.imports import *
from util.locations import *
from util.helpers import *
from util.objects import *
from optim.helpers import *

def permutation(journey: Journey, tanks: List[Tank], optimization_parameters: OptimizationParameters):
    # Get unused tanks
    unused_tanks = get_unused_tanks(journey=journey, tanks=tanks)

    # Select an unused tank 
    cpt = 0 
    for i, tank in enumerate(unused_tanks):
        # print(f"Tank {i}/{len(unused_tanks)}")
        unused_tanks_copy = deepcopy(unused_tanks)
        for tank_chosen in unused_tanks_copy:
            if tank.id == tank_chosen:
                # print(f"Current tank : {tank_chosen.id}")
                unused_tanks_copy.remove(tank_chosen)
                break 

        # Get the available positions to put the tank
        cycles_positions = get_available_cycles_positions(journey=journey, choice=tank_chosen, optimization_parameters=optimization_parameters)

        # Choose an available pair of cycle/position
        cycle_index, cycle_position = get_random_position(cycles_positions)

        if cycle_index is not None:
            new_cycle = optim_cycle(cycle=journey.cycles[cycle_index], choice=tank_chosen, choice_position=cycle_position, unused_tanks=unused_tanks_copy, optimization_parameters=optimization_parameters, method="D")
            
            if new_cycle is not None:
                new_journey = generate_neighbour_journey(journey=journey, new_cycle=new_cycle, cycle_index=cycle_index)

                if new_journey.evaluation(tanks=tanks)[0] >= journey.evaluation(tanks=tanks)[0]:
                    cpt += 1 

    print(f"Number of ameliorations : {cpt}/{len(unused_tanks)}")
