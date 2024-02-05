from util.imports import * 
from util.objects import *
from util.variables import *

def get_starting_time(tanks: List[Tank], agent: Agent, starting_constraint: datetime) -> datetime:
    all_start_times = []
    for tank in tanks:
        for hour_range in tank.maker.hours:
            all_start_times.append(hour_range[0])
    after_midnight_times = [start_time for start_time in all_start_times if start_time.time() > datetime.strptime('00:00', '%H:%M').time()]
    sorted_after_midnight_times = sorted(after_midnight_times)
    if sorted_after_midnight_times:
        if starting_constraint:
             return max(sorted_after_midnight_times[0], max(agent.begin_hour,starting_constraint))
        else : 
            return max(sorted_after_midnight_times[0], agent.begin_hour)
    else:
        return None
    
def get_coordinates(obj: Union[Tank, Storehouse]) -> Tuple[float, float]:
    if isinstance(obj, Tank):
        return radians(obj.maker.latitude), radians(obj.maker.longitude)
    else :
        return radians(obj.latitude), radians(obj.longitude)
    
def calculate_distance(obj1:  Union[Tank, Storehouse], obj2:  Union[Tank, Storehouse]) -> float:
    lat1, lon1 = get_coordinates(obj1)
    lat2, lon2 = get_coordinates(obj2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    R = 6371.0
    distance = R * c

    return distance

def get_available_tanks(starting_time: datetime, cycle: Cycle, tanks: List[Tank], storehouse: Storehouse, parameters: Parameters) -> List[Tank]:
    if cycle.selected_tanks:
        starting_point = cycle.selected_tanks[-1]
    else :
        starting_point = storehouse
        
    available_tanks = []
    for tank in tanks: 
        dist = calculate_distance(starting_point, tank)
        tank.time_to_go = ((60 * dist) / parameters.vehicle_speed) * K
        ending_time = starting_time + timedelta(minutes=tank.time_to_go)
        if tank.is_available(dt=ending_time):
            available_tanks.append(tank)
    return available_tanks

def get_valid_choices(tanks: List[Tank], cycle: Cycle, parameters: Parameters) -> List[Tank]:
    valid_tanks = []  
    for tank in tanks:
        if tank.current_volume <= parameters.mobile_tank_volume - cycle.total_volume:
            tank.collectable_volume = tank.current_volume
            valid_tanks.append(tank)
        else:
            if parameters.mobile_tank_volume - cycle.total_volume / tank.overflow_capacity >= parameters.percentage_partial_collect_volume:
                tank.collectable_volume = parameters.mobile_tank_volume - cycle.total_volume
                valid_tanks.append(tank)
    return valid_tanks

def check_storehouse_return(tanks: List[Tank], cycle: Cycle, storehouse: Storehouse, parameters: Parameters) -> List[Tank]:
    final_candidates = []
    for tank in tanks:
        tank.manoever_time = tank.collectable_volume / parameters.pumping_speed
        total_collect_time = tank.time_to_go + tank.manoever_time + parameters.loading_time
        tank.time_to_return = ((calculate_distance(tank, storehouse) * 60) / parameters.vehicle_speed) * K
        tank.potential_ending_time = (cycle.total_volume + tank.collectable_volume) / parameters.draining_speed
        if parameters.working_time*60 - cycle.total_time + total_collect_time + tank.time_to_return + tank.potential_ending_time + parameters.loading_time:
            final_candidates.append(tank)
    return final_candidates
            
def heuristical_choice(starting_point: Union[Tank, Storehouse], tanks: List[Tank], emergency=True) -> Tank:
    scores = []
    if emergency:
        for tank in tanks: 
            scores.append(weight_Q*tank.collectable_volume + weight_D*(calculate_distance(starting_point, tank)*K) - weight_E*(tank.current_volume/tank.overflow_capacity))
    else :
        for tank in tanks: 
            scores.append(weight_Q*tank.collectable_volume + weight_D*(calculate_distance(starting_point, tank)*K))
    return tanks[max(range(len(scores)), key=lambda i: scores[i])]



