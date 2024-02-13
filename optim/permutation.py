from util.imports import *
from util.locations import *
from util.helpers import *
from util.objects import *
from optim.helpers import *

def permutation(journey: Journey, tanks: List[Tank], optimization_parameters: OptimizationParameters):
    # Get unused tanks
    unused_tanks = get_unused_tanks(journey=journey, tanks=tanks)

    # Select an unused tank
    new_journeys = []
    for tank_index, tank_chosen in enumerate(unused_tanks):
        unused_tanks_copy = deepcopy(unused_tanks)
        # colored(tank_chosen.id, "cyan", "tank_chosen.id")
        # print("tank_chosen.id", tank_chosen.id)
        del unused_tanks_copy[tank_index]  # Supprime le réservoir choisi de la copie des réservoirs non utilisés

        # Get the available positions to put the tank
        cycles_positions = get_available_cycles_positions(journey=journey, choice=tank_chosen, optimization_parameters=optimization_parameters)

        # Choose an available pair of cycle/position
        for cycle_index, cycle_positions in enumerate(cycles_positions):
            for cycle_position in cycle_positions:
                # colored(cycle_index, "cyan")
                # colored(cycle_position, "cyan")

                # print("cycle_index", cycle_index)
                # print("cycle_position", cycle_position)

                # Optimize the cycle that needs to be changed
                for method in METHODS:
                    target_cycle = deepcopy(journey.cycles[cycle_index])
                    new_cycle = optim_cycle(cycle=target_cycle, choice=deepcopy(tank_chosen), choice_position=cycle_position, unused_tanks=deepcopy(unused_tanks_copy), optimization_parameters=optimization_parameters, method=method)
                    
                    if new_cycle is not None:
                        # print('new_journey generated')
                        new_journey = generate_neighbour_journey(journey=deepcopy(journey), new_cycle=new_cycle, cycle_index=cycle_index)
                        # print(json.dumps(new_journey.to_dict(), indent=4), "red", "Journey")  
                        new_journeys.append(new_journey)

    return new_journeys
