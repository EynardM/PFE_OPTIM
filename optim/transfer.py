from util.imports import *
from util.locations import *
from util.helpers import *
from util.objects import *

from algorithms.helpers import *
from algorithms.run import *

def get_selected_tanks_ids(journey: Journey):
    selected_tanks_ids = []
    for cycle in journey.cycles:
        for tank in cycle.selected_tanks:
            selected_tanks_ids.append(tank.id)
    return selected_tanks_ids

def get_reduced_tanks(select_tank_id: int, tanks: List[Tank]):
    reduced_tanks = deepcopy(tanks)
    for tank in reduced_tanks:
        if tank.id == select_tank_id:
            reduced_tanks.remove(tank)
    return reduced_tanks

def transfer(journey: Journey, tanks: List[Tank], optimization_parameters: OptimizationParameters):
    selected_tanks_ids = get_selected_tanks_ids(journey=journey)
    new_journeys = []
    for tank_id in selected_tanks_ids:
        reduced_tanks = get_reduced_tanks(select_tank_id=tank_id, tanks=tanks)
        optimization_parameters.tanks = reduced_tanks
        
        if optimization_parameters.agent.nb_of_slots() == 1:
            starting_time, ending_time = optimization_parameters.agent.daily_working_slot
            new_journey = Journey(starting_time=starting_time, ending_time=ending_time)
            new_journey = run_slot(journey=new_journey, optimization_parameters=optimization_parameters, slot=optimization_parameters.agent.daily_working_slot)
        else :
            for i,slot in enumerate(optimization_parameters.agent.daily_working_slot):
                if i == 0:
                    starting_time, ending_time = slot
                    new_journey = Journey(starting_time=starting_time, ending_time=ending_time) 
                    new_journey = run_slot(journey=new_journey, optimization_parameters=optimization_parameters, slot=slot)
                else :
                    new_journey = run_slot(journey=new_journey, optimization_parameters=optimization_parameters, slot=slot)

        new_journeys.append(new_journey)
    return new_journeys