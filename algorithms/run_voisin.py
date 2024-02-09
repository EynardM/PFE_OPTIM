from util.imports import * 
from util.objects import *
from util.helpers import *
from util.common import *

from algorithms.helpers import *

logging.basicConfig(level=logging.INFO)
file_handler = logging.FileHandler('logs/run_voisin.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_handler)

def run_voisin(cycle_index, choice_position, choice, journey, tanks, parameters, storehouse, agent, method):    
    processing_journey = True
    new_journey = Journey(start_time=journey.start_time, end_time=journey.end_time)

    for i, cycle in enumerate(journey.cycles):
        if i != cycle_index:
            new_journey.add_cycle(cycle=cycle)
        else:
            start = cycle.starting_time
        
    starting_constraint = deepcopy(start)

    while(processing_journey):
        starting_time = get_starting_time(tanks=tanks, agent=agent, starting_constraint=starting_constraint)
        processing_cycle = True
        cycle = Cycle(starting_time=starting_time)
        
        while(processing_cycle):

            if starting_constraint >= journey.end_time:
                processing_cycle = False
                processing_journey = False
                continue

            available_tanks = get_available_tanks(starting_time=starting_time+timedelta(minutes=cycle.cycle_time), cycle=cycle, tanks=tanks, storehouse=storehouse, parameters=parameters)  
            if not available_tanks:
                if not cycle.is_empty():
                    cycle.storehouse_return(parameters=parameters)
                    journey.add_cycle(cycle=cycle)
                    starting_constraint = cycle.starting_time + timedelta(minutes=cycle.cycle_time)
                else :
                    datetime_to_add = (starting_constraint + timedelta(hours=1)).replace(minute=0, second=0) - starting_constraint
                    cycle.cycle_time += datetime_to_add.total_seconds() / 60
                    journey.add_cycle(cycle=cycle)
                    starting_constraint += datetime_to_add
                processing_cycle = False
                continue

            valid_tanks = get_valid_choices(tanks=available_tanks, cycle=cycle, parameters=parameters)
            if not valid_tanks:
                cycle.storehouse_return(parameters=parameters)
                journey.add_cycle(cycle=cycle)
                starting_constraint = cycle.starting_time + timedelta(minutes=cycle.cycle_time)
                processing_cycle = False
                continue

            final_candidates = check_storehouse_return(journey=journey, tanks=valid_tanks, cycle=cycle, storehouse=storehouse, parameters=parameters)
            if not final_candidates:
                if not cycle.is_empty():
                    cycle.storehouse_return(parameters=parameters)
                    journey.add_cycle(cycle=cycle)
                    starting_constraint = cycle.starting_time + timedelta(minutes=cycle.cycle_time)
                processing_journey = False
                processing_cycle = False
                continue
            
            else : 
                last_point = cycle.get_last_point(storehouse=storehouse)
                tank = choice_function(starting_point=last_point, tanks=final_candidates, method=method)
                tanks.remove(tank)
                cycle.add_tank(choice=tank, parameters=parameters)
            
    for cycle in journey.cycles:
        print(cycle)
    return journey 


if __name__ == "__main__":
    run_voisin()