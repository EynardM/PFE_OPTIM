from util.imports import *
from util.locations import *
from util.helpers import *
from util.objects import *
from algorithms.helpers import *

def get_unused_tanks(journey: Journey, tanks: List[Tank]):
    unused_tanks = deepcopy(tanks)
    for cycle in journey.cycles:
        for tank_cycle in cycle.selected_tanks:
            for tank in unused_tanks:
                if tank_cycle.id == tank.id:
                    unused_tanks.remove(tank)
                    break 
    return unused_tanks

def is_available(starting_time: datetime, cycle: Cycle, choice: Tank, optimization_parameters: OptimizationParameters):
    last_point = cycle.get_last_point(storehouse=optimization_parameters.storehouse)
    time_to_go = ((calculate_distance(last_point, choice) * 60) / optimization_parameters.vehicle.speed) * K
    ending_time = starting_time + timedelta(minutes=time_to_go)
    return choice.is_available(dt=ending_time)

def get_available_cycles_positions(journey: Journey, choice: Tank, optimization_parameters: OptimizationParameters):
    cycles_positions = []
    for cycle in journey.cycles:
        cycle_positions = []
        current_time = cycle.starting_time
        if is_available(starting_time=current_time, cycle=cycle, choice=choice, optimization_parameters=optimization_parameters):
            cycle_positions.append(-1)
        for i in range(len(cycle.selected_tanks)):
            current_time += timedelta(minutes=cycle.travel_times[i]+cycle.manoever_times[i]+optimization_parameters.vehicle.loading_time)
            if is_available(starting_time=current_time, cycle=cycle, choice=choice, optimization_parameters=optimization_parameters):
                cycle_positions.append(i)
        cycles_positions.append(cycle_positions)
    return cycles_positions

def get_random_position(cycles_positions):
    cycles_positions_tmp = [(index, cycle_position) for index, cycle_position in enumerate(cycles_positions) if cycle_position]

    if cycles_positions_tmp:
        index, cycle_position_tmp = random.choice(cycles_positions_tmp)
        position = random.choice(cycle_position_tmp)
        return index, position
    else:
        return None, None