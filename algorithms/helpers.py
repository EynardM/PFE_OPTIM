from util.imports import * 
from util.objects import *
from util.variables import *
from util.helpers import *

# Main functions 

def generate_time_slots(tanks: List[Tank], constraints: Constraints, agent: Agent) -> List[Tuple[datetime]]:
    # Getting the global time range 
    all_start_times = []
    all_end_times = []
    for tank in tanks:
        for hour_range in tank.maker.hours:
            all_start_times.append(hour_range[0])
            all_end_times.append(hour_range[1])
    
    all_start_times = [start_time for start_time in all_start_times if start_time.time() > datetime.strptime('00:00', '%H:%M').time()]
    
    start = max(min(all_start_times), agent.begin_hour)
    end = max(all_end_times)
    
    # Generate working slots without break
    time_slots_without_break = []
    current_time = start
    while current_time + timedelta(hours=constraints.max_working_time) <= end:
        end_time = current_time + timedelta(hours=constraints.max_working_time)
        time_slots_without_break.append((current_time, end_time))
        current_time += timedelta(hours=1)

    # Generate working slots with break
    time_slots = []
    current_time = start
    while current_time + timedelta(hours=constraints.max_working_time+ BREAK_TIME) <= end:
        end_time = current_time + timedelta(hours=constraints.max_working_time+ BREAK_TIME)
        time_slots.append((current_time, end_time))
        current_time += timedelta(hours=1)

    time_slots_with_break = []
    for time_slot in time_slots:
        new_slot_start = time_slot[0] + timedelta(hours=BREAK_TIME)  # Ne pas commencer par une pause
        new_slot_end = time_slot[1] - timedelta(hours=BREAK_TIME)    # Ne pas finir par une pause
        for break_start in range(new_slot_start.hour, new_slot_end.hour):
            break_end = break_start + BREAK_TIME
            if break_end <= new_slot_end.hour:
                new_start = datetime(start.year, start.month, start.day, break_start, 0)
                new_end = datetime(start.year, start.month, start.day, break_end, 0)
                time_slots_with_break.append(((time_slot[0], new_start), (new_end, time_slot[1])))
    
    return time_slots_without_break + time_slots_with_break

def generate_optimization_paremeters(tanks: List[Tank], constraints: Constraints, vehicle: Vehicle, storehouse: Storehouse, agent: Agent, time_slots: List[Tuple[datetime]]) -> List[OptimizationParameters]:
    current_date = datetime.now()
    optimization_parameters_list = []
    for method in ["Random", "R", "Q", "D", "E", "HQD", "HQE", "HDE", "HQDE"]:
        for time_slot in time_slots:
            new_agent = deepcopy(agent)
            new_agent.daily_working_slot = time_slot
            optimization_parameters = OptimizationParameters(
                agent=new_agent,
                storehouse=storehouse,
                date=current_date,
                tanks=deepcopy(tanks),
                constraints=constraints,
                vehicle=vehicle,
                collector=None,
                method=method
            )
            optimization_parameters.agent.daily_working_slot = time_slot
            optimization_parameters_list.append(optimization_parameters)
    return optimization_parameters_list

# Run functions

def get_starting_time(journey: Journey, optimization_parameters: OptimizationParameters) -> datetime:
    all_start_times = []
    for tank in optimization_parameters.tanks:
        for hour_range in tank.maker.hours:
            all_start_times.append(hour_range[0])
    after_midnight_times = [start_time for start_time in all_start_times if start_time.time() > datetime.strptime('00:00', '%H:%M').time()]
    sorted_after_midnight_times = sorted(after_midnight_times)
    if sorted_after_midnight_times:
        return max(sorted_after_midnight_times[0], max(optimization_parameters.agent.begin_hour,journey.current_time))
    else:
        return None
    
def calculate_distance(obj1:  Union[Tank, Storehouse], obj2:  Union[Tank, Storehouse]) -> float:
    lat1, lon1 = obj1.get_coordinates()
    lat2, lon2 = obj2.get_coordinates()

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    R = 6371.0
    distance = R * c

    return distance

def filter_hours(journey: Journey, cycle: Cycle, optimization_parameters: OptimizationParameters) -> List[Tank]:
    last_point = cycle.get_last_point(storehouse=optimization_parameters.storehouse)
    available_tanks = []
    for tank in optimization_parameters.tanks: 
        tank.distance = calculate_distance(last_point, tank)
        tank.time_to_go = ((tank.distance * 60) / optimization_parameters.vehicle.speed) * K
        ending_time = journey.current_time + timedelta(minutes=tank.time_to_go)
        if tank.is_available(dt=ending_time):
            available_tanks.append(tank)
    return available_tanks

def filter_enough_filled(tanks: List[Tank], journey: Journey, cycle: Cycle, optimization_parameters: OptimizationParameters) -> List[Tank]:
    filled_enough_tanks = []  
    for tank in optimization_parameters.tanks:
        if tank.current_volume <= optimization_parameters.vehicle.capacity - cycle.cycle_volume:
            tank.collectable_volume = tank.current_volume
            filled_enough_tanks.append(tank)
        else:
            if (optimization_parameters.vehicle.capacity - cycle.cycle_volume) / tank.overflow_capacity >= optimization_parameters.constraints.percentage_volume_threshold:
                tank.collectable_volume = optimization_parameters.vehicle.capacity - cycle.cycle_volume
                filled_enough_tanks.append(tank)
    return filled_enough_tanks

def filter_return(tanks: List[Tank], journey: Journey, cycle: Cycle, optimization_parameters: OptimizationParameters) -> List[Tank]:
    final_tanks = []
    for tank in tanks:
        tank.manoever_time = tank.collectable_volume / optimization_parameters.vehicle.pumping_speed
        total_collect_time = tank.time_to_go + tank.manoever_time + optimization_parameters.vehicle.loading_time
        tank.time_to_storehouse = ((calculate_distance(tank, optimization_parameters.storehouse) * 60) / optimization_parameters.vehicle.speed) * K
        tank.return_time = tank.time_to_storehouse + ((cycle.cycle_volume + tank.collectable_volume) / optimization_parameters.vehicle.draining_speed) + optimization_parameters.vehicle.loading_time
        remaining_time = (journey.ending_time.hour - journey.starting_time.hour)*60 - journey.journey_time
        if remaining_time - (cycle.cycle_time + total_collect_time + tank.return_time) > 0:
            final_tanks.append(tank)
    return final_tanks

def choice_function(starting_point: Union[Tank, Storehouse], tanks: List[Tank], method):
    methods = ["R", "Q", "D", "E", "HQD", "HQDE"]

    if method == "Random":
        method = random.choice(methods)
    if method == "R":
        tank_chosen = random.choice(tanks)
    if method == "Q":
        tank_chosen = max(tanks, key=lambda tank: tank.collectable_volume)
    if method == "D":
        tank_chosen = min(tanks, key=lambda tank: calculate_distance(starting_point, tank))
    if method == "E":
        tank_chosen = max(tanks, key=lambda tank: (tank.current_volume / tank.overflow_capacity))
    if method == "HQD":
        scores = [weight_Q*tank.collectable_volume + weight_D*(calculate_distance(starting_point, tank)) for tank in tanks]
        tank_chosen  = tanks[max(range(len(scores)), key=lambda i: scores[i])]
    if method == "HDE":
        scores = [weight_D*(calculate_distance(starting_point, tank)) + weight_E*(tank.current_volume/tank.overflow_capacity) for tank in tanks]
        tank_chosen  = tanks[max(range(len(scores)), key=lambda i: scores[i])]
    if method == "HQE":
        scores = [weight_Q*tank.collectable_volume + weight_E*(tank.current_volume/tank.overflow_capacity) for tank in tanks]
        tank_chosen  = tanks[max(range(len(scores)), key=lambda i: scores[i])]
    if method == "HQDE":
        scores = [weight_Q*tank.collectable_volume + weight_D*(calculate_distance(starting_point, tank)) + weight_E*(tank.current_volume/tank.overflow_capacity) for tank in tanks]
        tank_chosen  = tanks[max(range(len(scores)), key=lambda i: scores[i])]
    
    return tank_chosen