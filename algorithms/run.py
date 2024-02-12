from util.imports import * 
from util.objects import *
from util.helpers import *
from util.common import *

from algorithms.helpers import *

logging.basicConfig(level=logging.INFO)
file_handler = logging.FileHandler('logs/run.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_handler)

def run_slot(journey: Journey, optimization_parameters: OptimizationParameters, slot=Tuple[datetime,datetime]) -> List[Cycle]:
    if journey.current_time != journey.starting_time:
        journey.break_time += (slot[0] - journey.ending_time).total_seconds()/60
        journey.current_time = slot[0]
        journey.ending_time = slot[1]

    processing_journey = True
    while(processing_journey):
        starting_time = get_starting_time(journey=journey, optimization_parameters=optimization_parameters)
        
        processing_cycle = True
        cycle = Cycle(starting_time=starting_time)
        
        while(processing_cycle):

            if journey.current_time >= journey.ending_time:
                processing_cycle = False
                processing_journey = False
                continue

            available_tanks = filter_hours(journey=journey, cycle=cycle, optimization_parameters=optimization_parameters)  
           
            if not available_tanks:
                if not cycle.is_empty():
                    cycle.storehouse_return(optimization_parameters=optimization_parameters)
                    journey.add_cycle(cycle=cycle)
                    journey.current_time += timedelta(minutes=cycle.cycle_time)
                else :
                    datetime_to_add = (journey.current_time + timedelta(hours=1)).replace(minute=0, second=0) - journey.current_time
                    cycle.cycle_time += datetime_to_add.total_seconds() / 60
                    journey.add_cycle(cycle=cycle)
                    journey.current_time += timedelta(minutes=cycle.cycle_time)
                processing_cycle = False
                continue

            filled_enough_tanks = filter_enough_filled(tanks=available_tanks, journey=journey, cycle=cycle, optimization_parameters=optimization_parameters)
            if not filled_enough_tanks:
                cycle.storehouse_return(optimization_parameters=optimization_parameters)
                journey.add_cycle(cycle=cycle)
                journey.current_time += timedelta(minutes=cycle.cycle_time)
                processing_cycle = False
                continue

            final_candidates = filter_return(tanks=filled_enough_tanks, journey=journey, cycle=cycle, optimization_parameters=optimization_parameters)
            if not final_candidates:
                if not cycle.is_empty():
                    cycle.storehouse_return(optimization_parameters=optimization_parameters)
                    journey.add_cycle(cycle=cycle)
                    journey.current_time += timedelta(minutes=cycle.cycle_time)
                processing_journey = False
                processing_cycle = False
                continue
            
            else : 
                last_point = cycle.get_last_point(storehouse=optimization_parameters.storehouse)
                tank = choice_function(starting_point=last_point, tanks=final_candidates, method=optimization_parameters.method)
                cycle.add_tank(choice=tank, optimization_parameters=optimization_parameters)
                optimization_parameters.tanks.remove(tank)

    return journey 
      
def run(optimization_parameters: OptimizationParameters):
    if optimization_parameters.agent.nb_of_slots() == 1:
        starting_time, ending_time = optimization_parameters.agent.daily_working_slot
        journey = Journey(starting_time=starting_time, ending_time=ending_time)
        journey = run_slot(journey=journey, optimization_parameters=optimization_parameters, slot=optimization_parameters.agent.daily_working_slot)
    else :
        for i,slot in enumerate(optimization_parameters.agent.daily_working_slot):
            if i == 0:
                starting_time, ending_time = slot
                journey = Journey(starting_time=starting_time, ending_time=ending_time)      
            journey = run_slot(journey=journey, optimization_parameters=optimization_parameters, slot=slot)
    return journey
            