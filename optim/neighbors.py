from util.imports import *
from util.helpers import *
from util.objects import *

from optim.permutation import *
from optim.swap import *
from optim.transfer import *

def get_neighbors(best_journey: Journey, tanks: List[Tank], optimization_parameters: OptimizationParameters, maximum_complexity: bool, example=False):
    
    if not example:
        permutation_journeys = permutation(journey=best_journey, tanks=tanks, optimization_parameters=optimization_parameters, maximum_complexity=maximum_complexity)
        swap_journeys = swap(journey=best_journey, tanks=tanks, optimization_parameters=optimization_parameters, maximum_complexity=maximum_complexity)
        transfer_journeys = transfer(journey=best_journey, tanks=tanks, optimization_parameters=optimization_parameters, maximum_complexity=maximum_complexity)
        
        new_journeys = []
        if permutation_journeys is not None:
            new_journeys += permutation_journeys
        if swap_journeys is not None:
            new_journeys += swap_journeys
        if transfer_journeys is not None:
            new_journeys += transfer_journeys
        
        return new_journeys

    if example:
        permutation_journeys = permutation(journey=best_journey, tanks=tanks, optimization_parameters=optimization_parameters, maximum_complexity=maximum_complexity)
        swap_journeys = swap(journey=best_journey, tanks=tanks, optimization_parameters=optimization_parameters, maximum_complexity=maximum_complexity)
        transfer_journeys = transfer(journey=best_journey, tanks=tanks, optimization_parameters=optimization_parameters, maximum_complexity=maximum_complexity)
        
        return permutation_journeys, swap_journeys, transfer_journeys