from util.imports import *
from util.locations import *
from util.helpers import *
from util.objects import *

from algorithms.helpers import *

def get_unused_tanks(journey: Journey, tanks: List[Tank]):
    """
    Get a list of tanks that haven't been used in the journey.

    Args:
    - journey (Journey): Journey object representing the current journey.
    - tanks (List[Tank]): List of Tank objects.

    Returns:
    - List[Tank]: List of unused Tank objects.
    """
    unused_tanks = deepcopy(tanks)
    for cycle in journey.cycles:
        for tank_cycle in cycle.selected_tanks:
            for tank in unused_tanks:
                if tank_cycle.id == tank.id:
                    unused_tanks.remove(tank)
                    break 
    return unused_tanks

def is_available(starting_time: datetime, cycle: Cycle, choice: Tank, optimization_parameters: OptimizationParameters):
    """
    Check if a tank is available at a certain time within a cycle.

    Args:
    - starting_time (datetime): Starting time within the cycle.
    - cycle (Cycle): Cycle object.
    - choice (Tank): Tank object being considered.
    - optimization_parameters (OptimizationParameters): OptimizationParameters object.

    Returns:
    - bool: True if the tank is available, False otherwise.
    """
    last_point = cycle.get_last_point(storehouse=optimization_parameters.storehouse)
    time_to_go = ((calculate_distance(last_point, choice) * 60) / optimization_parameters.vehicle.speed) * K
    ending_time = starting_time + timedelta(minutes=time_to_go)
    return choice.is_available(dt=ending_time)

def get_available_cycles_positions(journey: Journey, choice: Tank, optimization_parameters: OptimizationParameters):
    """
    Get available positions within cycles where a tank can be inserted.

    Args:
    - journey (Journey): Journey object representing the current journey.
    - choice (Tank): Tank object being considered.
    - optimization_parameters (OptimizationParameters): OptimizationParameters object.

    Returns:
    - List[List[int]]: List of lists containing available positions for each cycle.
    """
    cycles_positions = []
    for cycle in journey.cycles:
        cycle_positions = []
        current_time = cycle.starting_time
        if is_available(starting_time=current_time, cycle=cycle, choice=choice, optimization_parameters=optimization_parameters):
            cycle_positions.append(-1)
        for i in range(len(cycle.selected_tanks)):
            current_time += timedelta(minutes=cycle.travel_times[i] + cycle.manoever_times[i] + optimization_parameters.vehicle.loading_time)
            if is_available(starting_time=current_time, cycle=cycle, choice=choice, optimization_parameters=optimization_parameters):
                cycle_positions.append(i)
        cycles_positions.append(cycle_positions)
    return cycles_positions

    
def get_unchanged_cycle(cycle: Cycle, choice_position: int, optimization_parameters: OptimizationParameters) -> Cycle:
    """
    Get a copy of the cycle up to the chosen position.

    Args:
    - cycle (Cycle): Cycle object.
    - choice_position (int): Position where the tank is inserted.
    - optimization_parameters (OptimizationParameters): OptimizationParameters object.

    Returns:
    - Cycle: Copy of the cycle with tanks selected up to the chosen position.
    """
    new_cycle = Cycle(starting_time=cycle.starting_time, ending_time=cycle.ending_time)

    # Update selected tanks, travel times, distances, and quantities
    new_cycle.selected_tanks = deepcopy(cycle.selected_tanks[:choice_position + 1])
    new_cycle.travel_times = cycle.travel_times[:choice_position + 1]
    new_cycle.travel_distances = cycle.travel_distances[:choice_position + 1]
    new_cycle.manoever_times = cycle.manoever_times[:choice_position + 1]
    new_cycle.collected_quantities = cycle.collected_quantities[:choice_position + 1]

    # Update cycle variables and current time
    new_cycle.cycle_time = sum(new_cycle.travel_times) + sum(new_cycle.manoever_times) + len(new_cycle.selected_tanks) * optimization_parameters.vehicle.loading_time
    new_cycle.cycle_distance = sum(new_cycle.travel_distances)
    new_cycle.cycle_volume = sum(new_cycle.collected_quantities)
    new_cycle.current_time = new_cycle.starting_time + timedelta(minutes=new_cycle.cycle_time)
    
    return new_cycle

def get_remaining_tanks(cycle: Cycle, choice_position: int, unused_tanks: List[Tank]):
    """
    Get a list of tanks remaining after inserting a tank into a cycle.

    Args:
    - cycle (Cycle): Cycle object.
    - choice_position (int): Position where the tank is inserted.
    - unused_tanks (List[Tank]): List of unused Tank objects.

    Returns:
    - List[Tank]: List of remaining Tank objects.
    """
    previous_tanks_from_cycle = cycle.selected_tanks[:choice_position + 1]
    previous_quantities_taken = cycle.collected_quantities[:choice_position + 1]
    remaining_tanks = unused_tanks + cycle.selected_tanks[:choice_position + 1]
    
    for i, tank in enumerate(previous_tanks_from_cycle):
        tank.current_volume += previous_quantities_taken[i]

    return remaining_tanks

def update_choice_attributes(cycle: Cycle, choice: Tank, optimization_parameters: OptimizationParameters):
    """
    Update attributes of the chosen tank based on the current cycle.

    Args:
    - cycle (Cycle): Cycle object.
    - choice (Tank): Tank object being considered.
    - optimization_parameters (OptimizationParameters): OptimizationParameters object.

    Returns:
    - None
    """
    last_point = cycle.get_last_point(storehouse=optimization_parameters.storehouse)
    
    # Update distance, travel time, and pumped volume attributes
    choice.distance = calculate_distance(last_point, choice)
    choice.time_to_go = ((choice.distance * 60) / optimization_parameters.vehicle.speed) * K
    if choice.current_volume <= optimization_parameters.vehicle.capacity - cycle.cycle_volume:
            choice.collectable_volume = choice.current_volume
    else:
        if (optimization_parameters.vehicle.capacity - cycle.cycle_volume) / choice.overflow_capacity >= optimization_parameters.constraints.percentage_volume_threshold:
            choice.collectable_volume = optimization_parameters.vehicle.capacity - cycle.cycle_volume
        else:
            choice.collectable_volume = 0

def check_choice(cycle: Cycle, choice: Tank, optimization_parameters: OptimizationParameters):
    """
    Check if the chosen tank can be accommodated within the cycle based on time constraints.

    Args:
    - cycle (Cycle): Cycle object.
    - choice (Tank): Tank object being considered.
    - optimization_parameters (OptimizationParameters): OptimizationParameters object.

    Returns:
    - bool: True if the tank can be accommodated, False otherwise.
    """
    choice.manoever_time = choice.collectable_volume / optimization_parameters.vehicle.pumping_speed
    total_collect_time = choice.time_to_go + choice.manoever_time + optimization_parameters.vehicle.loading_time
    choice.time_to_storehouse = ((calculate_distance(choice, optimization_parameters.storehouse) * 60) / optimization_parameters.vehicle.speed) * K
    choice.return_time = choice.time_to_storehouse + ((cycle.cycle_volume + choice.collectable_volume) / optimization_parameters.vehicle.draining_speed) + optimization_parameters.vehicle.loading_time
    total_time = (cycle.ending_time.hour - cycle.starting_time.hour) * 60
    remaining_time = total_time - (cycle.cycle_time + total_collect_time + choice.return_time)
    return remaining_time > 0

def filter_hours_cycle(cycle: Cycle, tanks: List[Tank], optimization_parameters: OptimizationParameters) -> List[Tank]:
    """
    Filter tanks based on their availability within a cycle.

    Args:
    - cycle (Cycle): Cycle object.
    - tanks (List[Tank]): List of Tank objects.
    - optimization_parameters (OptimizationParameters): OptimizationParameters object.

    Returns:
    - List[Tank]: List of available Tank objects within the cycle.
    """
    last_point = cycle.get_last_point(storehouse=optimization_parameters.storehouse)
    available_tanks = []
    for tank in tanks: 
        tank.distance = calculate_distance(last_point, tank)
        tank.time_to_go = ((tank.distance * 60) / optimization_parameters.vehicle.speed) * K
        ending_time = cycle.current_time + timedelta(minutes=tank.time_to_go)
        if tank.is_available(dt=ending_time):
            available_tanks.append(tank)
    return available_tanks

def filter_enough_filled_cycle(cycle: Cycle, tanks: List[Tank], optimization_parameters: OptimizationParameters) -> List[Tank]:
    """
    Filter tanks based on their filled capacity within a cycle.

    Args:
    - cycle (Cycle): Cycle object.
    - tanks (List[Tank]): List of Tank objects.
    - optimization_parameters (OptimizationParameters): OptimizationParameters object.

    Returns:
    - List[Tank]: List of Tank objects with enough capacity to fill.
    """
    filled_enough_tanks = []  
    for tank in tanks:
        if tank.current_volume <= optimization_parameters.vehicle.capacity - cycle.cycle_volume:
            tank.collectable_volume = tank.current_volume
            filled_enough_tanks.append(tank)
        else:
            if (optimization_parameters.vehicle.capacity - cycle.cycle_volume) / tank.overflow_capacity >= optimization_parameters.constraints.percentage_volume_threshold:
                tank.collectable_volume = optimization_parameters.vehicle.capacity - cycle.cycle_volume
                filled_enough_tanks.append(tank)
    return filled_enough_tanks

def filter_return_cycle(cycle: Cycle, tanks: List[Tank], optimization_parameters: OptimizationParameters) -> List[Tank]:
    """
    Filter tanks based on their return time within a cycle.

    Args:
    - cycle (Cycle): Cycle object.
    - tanks (List[Tank]): List of Tank objects.
    - optimization_parameters (OptimizationParameters): OptimizationParameters object.

    Returns:
    - List[Tank]: List of Tank objects with sufficient time to return.
    """
    final_tanks = []
    for tank in tanks:
        tank.manoever_time = tank.collectable_volume / optimization_parameters.vehicle.pumping_speed
        total_collect_time = tank.time_to_go + tank.manoever_time + optimization_parameters.vehicle.loading_time
        tank.time_to_storehouse = ((calculate_distance(tank, optimization_parameters.storehouse) * 60) / optimization_parameters.vehicle.speed) * K
        tank.return_time = tank.time_to_storehouse + ((cycle.cycle_volume + tank.collectable_volume) / optimization_parameters.vehicle.draining_speed) + optimization_parameters.vehicle.loading_time
        total_time = (cycle.ending_time.hour - cycle.starting_time.hour) * 60
        remaining_time = total_time - (cycle.cycle_time + total_collect_time + tank.return_time)
        if remaining_time > 0:
            final_tanks.append(tank)
    return final_tanks

def optim_cycle(cycle: Cycle, choice: Tank, choice_position: int, unused_tanks: List[Tank], optimization_parameters: OptimizationParameters, method):
    """
    Optimize a cycle by inserting a tank at a specific position.

    Args:
    - cycle (Cycle): Cycle object.
    - choice (Tank): Tank object to be inserted.
    - choice_position (int): Position in the cycle where the tank is inserted.
    - unused_tanks (List[Tank]): List of unused Tank objects.
    - optimization_parameters (OptimizationParameters): OptimizationParameters object.
    - method (str): Method for tank selection.

    Returns:
    - Cycle: Optimized Cycle object with the tank inserted.
    """
    # Slicing the cycle till the choice_position
    new_cycle = get_unchanged_cycle(cycle=cycle, choice_position=choice_position, optimization_parameters=optimization_parameters)

    # Get the list of remaining tanks for the optimization of the cycle
    remaining_tanks = get_remaining_tanks(cycle=cycle, choice_position=choice_position, unused_tanks=unused_tanks)

    # Updating the attributes of the chosen tank (depending on the sliced cycle) 
    update_choice_attributes(cycle=new_cycle, choice=choice, optimization_parameters=optimization_parameters)

    # Adding chosen tank 
    choice_flag = True
    processing_cycle = False
    if choice_flag:
        if check_choice(cycle=new_cycle, choice=choice, optimization_parameters=optimization_parameters):
            new_cycle.add_tank(choice=choice, optimization_parameters=optimization_parameters)
            choice_flag = False
            processing_cycle = True
        else :
            return None
    
    while(processing_cycle):
        # Applying the filters to know which tanks are available for a collect mission
        available_tanks = filter_hours_cycle(cycle=new_cycle, tanks=remaining_tanks, optimization_parameters=optimization_parameters)  
        filled_enough_tanks = filter_enough_filled_cycle(cycle=new_cycle, tanks=available_tanks, optimization_parameters=optimization_parameters)
        final_tanks = filter_return_cycle(cycle=new_cycle, tanks=filled_enough_tanks, optimization_parameters=optimization_parameters)
        
        if not final_tanks:
            processing_cycle = False
        else : 
            last_point = new_cycle.get_last_point(storehouse=optimization_parameters.storehouse)
            tank = choice_function(starting_point=last_point, tanks=final_tanks, method=method)
            new_cycle.add_tank(choice=tank, optimization_parameters=optimization_parameters)
            remaining_tanks.remove(tank)
    return new_cycle

def generate_neighbour_journey(journey: Journey, new_cycle: Cycle, cycle_index: int) -> Journey :
    """
    Generate a new journey by replacing a cycle with an optimized cycle.

    Args:
    - journey (Journey): Original Journey object.
    - new_cycle (Cycle): Optimized Cycle object to replace.
    - cycle_index (int): Index of the cycle to be replaced.

    Returns:
    - Journey: New Journey object with the optimized cycle.
    """
    new_journey = Journey(starting_time=journey.starting_time, ending_time=journey.ending_time)
    for i, cycle in enumerate(journey.cycles):
        if i != cycle_index:
            new_journey.add_cycle(cycle=cycle)
        else:
            new_journey.add_cycle(cycle=new_cycle)
    return new_journey

def permutation(journey: Journey, tanks: List[Tank], optimization_parameters: OptimizationParameters, maximum_complexity: bool):
    """
    Generate new journeys by permuting tanks within cycles.

    Args:
    - journey (Journey): Original Journey object.
    - tanks (List[Tank]): List of Tank objects.
    - optimization_parameters (OptimizationParameters): OptimizationParameters object.
    - maximum_complexity (bool): Flag to enable maximum complexity.

    Returns:
    - List[Journey]: List of new Journey objects with permutations.
    """
    # Get unused tanks
    unused_tanks = get_unused_tanks(journey=journey, tanks=tanks)

    # Select an unused tank
    new_journeys = []
    if maximum_complexity:
        for tank_index, tank_chosen in enumerate(unused_tanks):
            unused_tanks_copy = deepcopy(unused_tanks)
            del unused_tanks_copy[tank_index]  

            # Get the available positions to put the tank
            cycles_positions = get_available_cycles_positions(journey=journey, choice=tank_chosen, optimization_parameters=optimization_parameters)

            # Choose an available pair of cycle/position
            for cycle_index, cycle_positions in enumerate(cycles_positions):
                for cycle_position in cycle_positions:

                    # Optimize the cycle that needs to be changed
                    for method in METHODS:
                        target_cycle = deepcopy(journey.cycles[cycle_index])
                        new_cycle = optim_cycle(cycle=target_cycle, choice=deepcopy(tank_chosen), choice_position=cycle_position, unused_tanks=deepcopy(unused_tanks_copy), optimization_parameters=optimization_parameters, method=method)
                        
                        if new_cycle is not None:
                            new_journey = generate_neighbour_journey(journey=deepcopy(journey), new_cycle=new_cycle, cycle_index=cycle_index)
                            new_journeys.append(new_journey)
    else:
        tank_chosen = random.choice(unused_tanks)
        tank_index = unused_tanks.index(tank_chosen)
        unused_tanks_copy = deepcopy(unused_tanks)
        del unused_tanks_copy[tank_index]  

        # Get the available positions to put the tank
        cycles_positions = get_available_cycles_positions(journey=journey, choice=tank_chosen, optimization_parameters=optimization_parameters)

        # Choose an available pair of cycle/position
        for cycle_index, cycle_positions in enumerate(cycles_positions):
            for cycle_position in cycle_positions:

                # Optimize the cycle that needs to be changed
                for method in METHODS:
                    target_cycle = deepcopy(journey.cycles[cycle_index])
                    new_cycle = optim_cycle(cycle=target_cycle, choice=deepcopy(tank_chosen), choice_position=cycle_position, unused_tanks=deepcopy(unused_tanks_copy), optimization_parameters=optimization_parameters, method=method)
                    
                    if new_cycle is not None:
                        new_journey = generate_neighbour_journey(journey=deepcopy(journey), new_cycle=new_cycle, cycle_index=cycle_index)
                        new_journeys.append(new_journey)
    return new_journeys
