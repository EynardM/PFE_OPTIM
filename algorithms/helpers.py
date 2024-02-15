from util.imports import * 
from util.objects import *
from util.variables import *
from util.helpers import *

def generate_time_slots(tanks: List[Tank], constraints: Constraints, agent: Agent) -> List[Tuple[datetime]]:
    """
    Generates time slots based on tank availability, agent constraints, and working hours.
    
    Args:
    - tanks (List[Tank]): List of Tank objects representing availability schedules.
    - constraints (Constraints): Constraints object representing agent's working constraints.
    - agent (Agent): Agent object containing information about the agent's working hours.
    
    Returns:
    - List[Tuple[datetime]]: List of time slots available for the agent to work.
    """

    # Getting the global time range 
    all_start_times = []
    all_end_times = []
    for tank in tanks:
        for hour_range in tank.maker.hours:
            all_start_times.append(hour_range[0])
            all_end_times.append(hour_range[1])

    # Filter out start times before 00:00
    all_start_times = [start_time for start_time in all_start_times if start_time.time() > datetime.strptime('00:00', '%H:%M').time()]

    # Determine start and end times within global range and agent's begin_hour
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

    # Generate time slots considering break times
    time_slots_with_break = []
    for time_slot in time_slots:
        new_slot_start = time_slot[0] + timedelta(hours=BREAK_TIME)  # Avoid starting with a break
        new_slot_end = time_slot[1] - timedelta(hours=BREAK_TIME)    # Avoid ending with a break
        for break_start in range(new_slot_start.hour, new_slot_end.hour):
            break_end = break_start + BREAK_TIME
            if break_end <= new_slot_end.hour:
                new_start = datetime(start.year, start.month, start.day, break_start, 0)
                new_end = datetime(start.year, start.month, start.day, break_end, 0)
                time_slots_with_break.append(((time_slot[0], new_start), (new_end, time_slot[1])))

    # Combine time slots without and with break
    return time_slots_without_break + time_slots_with_break

def generate_optimization_paremeters(tanks: List[Tank], constraints: Constraints, vehicle: Vehicle, storehouse: Storehouse, agent: Agent, time_slots: List[Tuple[datetime]]) -> List[OptimizationParameters]:
    """
    Generate a list of optimization parameters for various methods and time slots.

    Args:
        tanks (List[Tank]): List of tanks.
        constraints (Constraints): Object containing constraints.
        vehicle (Vehicle): Object representing the vehicle.
        storehouse (Storehouse): Object representing the storehouse.
        agent (Agent): Object representing the agent.
        time_slots (List[Tuple[datetime]]): List of time slots.

    Returns:
        List[OptimizationParameters]: List of optimization parameters for different methods and time slots.
    """
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

def get_starting_time(journey: Journey, optimization_parameters: OptimizationParameters) -> datetime:
    """
    Determines the starting time for a journey based on tank availability and agent constraints.

    Args:
    - journey (Journey): Journey object representing the current journey.
    - optimization_parameters (OptimizationParameters): OptimizationParameters object containing tank and agent information.

    Returns:
    - datetime: Starting time for the journey.
    """
    # Extract all available start times for tanks
    all_start_times = []
    for tank in optimization_parameters.tanks:
        for hour_range in tank.maker.hours:
            all_start_times.append(hour_range[0])
    
    # Filter out times after midnight
    after_midnight_times = [start_time for start_time in all_start_times if start_time.time() > datetime.strptime('00:00', '%H:%M').time()]
    
    # Sort the filtered times
    sorted_after_midnight_times = sorted(after_midnight_times)
    
    # Determine the starting time based on constraints and availability
    if sorted_after_midnight_times:
        return max(sorted_after_midnight_times[0], max(optimization_parameters.agent.begin_hour, journey.current_time))
    else:
        return None

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
    
def calculate_distance(obj1: Union[Tank, Storehouse], obj2: Union[Tank, Storehouse]) -> float:
    """
    Calculates the distance between two geographical coordinates using Haversine formula.

    Args:
    - obj1 (Union[Tank, Storehouse]): Object with latitude and longitude coordinates.
    - obj2 (Union[Tank, Storehouse]): Object with latitude and longitude coordinates.

    Returns:
    - float: Distance between the two objects in kilometers.
    """
    lat1, lon1 = obj1.get_coordinates()
    lat2, lon2 = obj2.get_coordinates()

    # Calculate differences in latitude and longitude
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Apply Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    R = 6371.0  # Earth radius in kilometers
    distance = R * c

    return distance

def filter_hours(cycle: Cycle, optimization_parameters: OptimizationParameters) -> List[Tank]:
    """
    Filters available tanks based on distance and time constraints.

    Args:
    - cycle (Cycle): Cycle object representing the current cycle.
    - optimization_parameters (OptimizationParameters): OptimizationParameters object containing tank and vehicle information.

    Returns:
    - List[Tank]: List of tanks that satisfy distance and time constraints.
    """
    last_point = cycle.get_last_point(storehouse=optimization_parameters.storehouse)
    available_tanks = []

    # Iterate over tanks and filter based on distance and time constraints
    for tank in optimization_parameters.tanks: 
        tank.distance = calculate_distance(last_point, tank)
        tank.time_to_go = ((tank.distance * 60) / optimization_parameters.vehicle.speed) * K
        ending_time = cycle.current_time + timedelta(minutes=tank.time_to_go)
        if tank.is_available(dt=ending_time):
            available_tanks.append(tank)

    return available_tanks

def filter_enough_filled(tanks: List[Tank], cycle: Cycle, optimization_parameters: OptimizationParameters) -> List[Tank]:
    """
    Filters tanks based on their fill level and capacity.

    Args:
    - tanks (List[Tank]): List of tanks to be filtered.
    - cycle (Cycle): Cycle object representing the current cycle.
    - optimization_parameters (OptimizationParameters): OptimizationParameters object containing vehicle information.

    Returns:
    - List[Tank]: List of tanks that have sufficient capacity to collect additional volume.
    """
    filled_enough_tanks = []  

    # Iterate over tanks and filter based on fill level and capacity
    for tank in tanks:
        if tank.current_volume <= optimization_parameters.vehicle.capacity - cycle.cycle_volume:
            tank.collectable_volume = tank.current_volume
            filled_enough_tanks.append(tank)
        else:
            if (optimization_parameters.vehicle.capacity - cycle.cycle_volume) / tank.overflow_capacity >= optimization_parameters.constraints.percentage_volume_threshold:
                tank.collectable_volume = optimization_parameters.vehicle.capacity - cycle.cycle_volume
                filled_enough_tanks.append(tank)

    return filled_enough_tanks

def filter_return(tanks: List[Tank], journey: Journey, cycle: Cycle, optimization_parameters: OptimizationParameters) -> List[Tank]:
    """
    Filters tanks based on return time constraints.

    Args:
    - tanks (List[Tank]): List of tanks to be filtered.
    - journey (Journey): Journey object representing the current journey.
    - cycle (Cycle): Cycle object representing the current cycle.
    - optimization_parameters (OptimizationParameters): OptimizationParameters object containing vehicle information.

    Returns:
    - List[Tank]: List of tanks that satisfy return time constraints.
    """
    final_tanks = []

    # Iterate over tanks and filter based on return time constraints
    for tank in tanks:
        tank.manoever_time = tank.collectable_volume / optimization_parameters.vehicle.pumping_speed
        total_collect_time = tank.time_to_go + tank.manoever_time + optimization_parameters.vehicle.loading_time
        tank.time_to_storehouse = ((calculate_distance(tank, optimization_parameters.storehouse) * 60) / optimization_parameters.vehicle.speed) * K
        tank.return_time = tank.time_to_storehouse + ((cycle.cycle_volume + tank.collectable_volume) / optimization_parameters.vehicle.draining_speed) + optimization_parameters.vehicle.loading_time
        remaining_datetime = journey.ending_time - journey.current_time
        if remaining_datetime > timedelta(minutes=(cycle.cycle_time + total_collect_time + tank.return_time)):
            final_tanks.append(tank)

    return final_tanks

def choice_function(starting_point: Union[Tank, Storehouse], tanks: List[Tank], method: str) -> Union[Tank, None]:
    """
    Chooses a tank based on a specified method.

    Args:
    - starting_point (Union[Tank, Storehouse]): Starting point for the selection.
    - tanks (List[Tank]): List of tanks to choose from.
    - method (str): Method for tank selection.

    Returns:
    - Union[Tank, None]: Chosen tank based on the method, or None if no valid tank is chosen.
    """
    # Randomly choose a method if specified as 'Random'
    if method == "Random":
        method = random.choice(METHODS)

    # Apply specified method for tank selection
    if method == "R":
        tank_chosen = random.choice(tanks)
    if method == "Q":
        tank_chosen = max(tanks, key=lambda tank: tank.collectable_volume)
    if method == "D":
        tank_chosen = min(tanks, key=lambda tank: calculate_distance(starting_point, tank))
    if method == "E":
        tank_chosen = max(tanks, key=lambda tank: ((tank.current_volume + tank.mean_filling) / tank.overflow_capacity))
    if method == "HQD":
        scores = [weight_Q*tank.collectable_volume + weight_D*(calculate_distance(starting_point, tank)) for tank in tanks]
        tank_chosen = tanks[max(range(len(scores)), key=lambda i: scores[i])]
    if method == "HDE":
        scores = [weight_D*(calculate_distance(starting_point, tank)) + weight_E*((tank.current_volume + tank.mean_filling)/tank.overflow_capacity) for tank in tanks]
        tank_chosen = tanks[max(range(len(scores)), key=lambda i: scores[i])]
    if method == "HQE":
        scores = [weight_Q*tank.collectable_volume + weight_E*((tank.current_volume + tank.mean_filling)/tank.overflow_capacity) for tank in tanks]
        tank_chosen = tanks[max(range(len(scores)), key=lambda i: scores[i])]
    if method == "HQDE":
        scores = [weight_Q*tank.collectable_volume + weight_D*(calculate_distance(starting_point, tank)) + weight_E*((tank.current_volume + tank.mean_filling)/tank.overflow_capacity) for tank in tanks]
        tank_chosen = tanks[max(range(len(scores)), key=lambda i: scores[i])]

    return tank_chosen