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
    
# Optim cycle functions
    
def get_unchanged_cycle(cycle: Cycle, choice_position: int, optimization_parameters: OptimizationParameters) -> Cycle:
    new_cycle = Cycle(starting_time=cycle.starting_time, ending_time=cycle.ending_time)

    # Updating selected tanks
    new_cycle.selected_tanks = deepcopy(cycle.selected_tanks[:choice_position+1])

    # Updating travel times distances and quantities
    new_cycle.travel_times = cycle.travel_times[:choice_position+1]
    new_cycle.travel_distances = cycle.travel_distances[:choice_position+1]
    new_cycle.manoever_times = cycle.manoever_times[:choice_position+1]
    new_cycle.collected_quantities = cycle.collected_quantities[:choice_position+1]

    # Updating cycle variables
    new_cycle.cycle_time = sum(new_cycle.travel_times) + sum(new_cycle.manoever_times) + len(new_cycle.selected_tanks) * optimization_parameters.vehicle.loading_time
    new_cycle.cycle_distance = sum(new_cycle.travel_distances)
    new_cycle.cycle_volume = sum(new_cycle.collected_quantities)

    # Updating current time
    new_cycle.current_time = new_cycle.starting_time + timedelta(minutes=new_cycle.cycle_time)
    
    return new_cycle

def get_remaining_tanks(cycle: Cycle, choice_position: int, unused_tanks: List[Tank]):
    previous_tanks_from_cycle = cycle.selected_tanks[:choice_position+1]
    previous_quantities_taken = cycle.collected_quantities[:choice_position+1]
    remaining_tanks = unused_tanks + cycle.selected_tanks[:choice_position+1]
    
    for i, tank in enumerate(previous_tanks_from_cycle):
        tank.current_volume += previous_quantities_taken[i]

    return remaining_tanks

def update_choice_attributes(cycle: Cycle, choice: Tank, optimization_parameters: OptimizationParameters):
    last_point = cycle.get_last_point(storehouse=optimization_parameters.storehouse)
    
    # Distance
    choice.distance = calculate_distance(last_point, choice)

    # Travel time
    choice.time_to_go = ((choice.distance * 60) / optimization_parameters.vehicle.speed) * K

    # Pumped volume
    if choice.current_volume <= optimization_parameters.vehicle.capacity - cycle.cycle_volume:
            choice.collectable_volume = choice.current_volume
    else:
        if (optimization_parameters.vehicle.capacity - cycle.cycle_volume) / choice.overflow_capacity >= optimization_parameters.constraints.percentage_volume_threshold:
            choice.collectable_volume = optimization_parameters.vehicle.capacity - cycle.cycle_volume
        else :
            choice.collectable_volume = 0

def check_choice(cycle: Cycle, choice: Tank, optimization_parameters: OptimizationParameters):
    choice.manoever_time = choice.collectable_volume / optimization_parameters.vehicle.pumping_speed
    total_collect_time = choice.time_to_go + choice.manoever_time + optimization_parameters.vehicle.loading_time
    choice.time_to_storehouse = ((calculate_distance(choice, optimization_parameters.storehouse) * 60) / optimization_parameters.vehicle.speed) * K
    choice.return_time = choice.time_to_storehouse + ((cycle.cycle_volume + choice.collectable_volume) / optimization_parameters.vehicle.draining_speed) + optimization_parameters.vehicle.loading_time
    total_time = (cycle.ending_time.hour - cycle.starting_time.hour)*60
    remaining_time = total_time - (cycle.cycle_time + total_collect_time + choice.return_time)
    return remaining_time > 0

def filter_hours_cycle(cycle: Cycle, tanks: List[Tank], optimization_parameters: OptimizationParameters) -> List[Tank]:
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
    final_tanks = []
    for tank in tanks:
        tank.manoever_time = tank.collectable_volume / optimization_parameters.vehicle.pumping_speed
        total_collect_time = tank.time_to_go + tank.manoever_time + optimization_parameters.vehicle.loading_time
        tank.time_to_storehouse = ((calculate_distance(tank, optimization_parameters.storehouse) * 60) / optimization_parameters.vehicle.speed) * K
        tank.return_time = tank.time_to_storehouse + ((cycle.cycle_volume + tank.collectable_volume) / optimization_parameters.vehicle.draining_speed) + optimization_parameters.vehicle.loading_time
        total_time = (cycle.ending_time.hour - cycle.starting_time.hour)*60
        remaining_time = total_time - (cycle.cycle_time + total_collect_time + tank.return_time)
        if remaining_time > 0:
            final_tanks.append(tank)
    return final_tanks

def optim_cycle(cycle: Cycle, choice: Tank, choice_position: int, unused_tanks: List[Tank], optimization_parameters: OptimizationParameters, method):
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
            # if new_cycle.current_time < new_cycle.ending_time:
            #     new_cycle.ending_time = new_cycle.current_time
            processing_cycle = False
        else : 
            last_point = new_cycle.get_last_point(storehouse=optimization_parameters.storehouse)
            tank = choice_function(starting_point=last_point, tanks=final_tanks, method=method)
            new_cycle.add_tank(choice=tank, optimization_parameters=optimization_parameters)
            remaining_tanks.remove(tank)
    return new_cycle

def generate_neighbour_journey(journey: Journey, new_cycle: Cycle, cycle_index: int) -> Journey :
    new_journey = Journey(starting_time=journey.starting_time, ending_time=journey.ending_time)
    for i, cycle in enumerate(journey.cycles):
        if i != cycle_index:
            new_journey.add_cycle(cycle=cycle)
        else:
            new_journey.add_cycle(cycle=new_cycle)
    return new_journey

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
