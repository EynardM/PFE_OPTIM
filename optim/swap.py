from util.imports import *
from util.locations import *
from util.helpers import *
from util.objects import *

from algorithms.helpers import *

def get_couples(journey: Journey):
    tanks_arriving_time = {}
    for cycle in journey.cycles:
        current_time = cycle.starting_time
        for i, tank in enumerate(cycle.selected_tanks):
            current_time += timedelta(minutes=cycle.travel_times[i])
            tanks_arriving_time[tank] = current_time
    return tanks_arriving_time

def available_swap(tank1, time1, tank2, time2):
    if tank2.is_available(dt=time1) and tank1.is_available(dt=time2):
        return True
    return False

def get_possible_swaps(tank_time: dict):
    possible_swaps = []
    for tank1, time1 in tank_time.items():
        for tank2, time2 in tank_time.items():
            if tank1 != tank2:
                if available_swap(tank1=tank1, time1=time1, tank2=tank2, time2=time2):
                    possible_swaps.append([tank1, tank2])
    return possible_swaps

def get_cycles_tanks(journey: Journey, pair: Tuple[Tank, Tank]):
    tank1, tank2 = pair
    cycles_selected_tanks = []
    for cycle_index, cycle in enumerate(journey.cycles):
        cycle_selected_tanks = []
        for tank_position, tank in enumerate(cycle.selected_tanks):
            if tank.id == tank1.id:
                cycle_selected_tanks.append(tank2)
            elif tank.id == tank2.id:
                cycle_selected_tanks.append(tank1)
            else:
                cycle_selected_tanks.append(tank)
        cycles_selected_tanks.append(cycle_selected_tanks)
    return cycles_selected_tanks

def update_current_volume(selected_tank: Tank, tanks: List[Tank]):
    for tank in tanks:
        if selected_tank.id == tank.id:
            selected_tank.current_volume = tank.current_volume
            break 

def update_attributes(cycle: Cycle, tank: Tank, optimization_parameters: OptimizationParameters):
    last_point = cycle.get_last_point(storehouse=optimization_parameters.storehouse)
    
    # Distance
    tank.distance = calculate_distance(last_point, tank)

    # Travel time
    tank.time_to_go = ((tank.distance * 60) / optimization_parameters.vehicle.speed) * K

    # Pumped volume
    if tank.current_volume <= optimization_parameters.vehicle.capacity - cycle.cycle_volume:
            tank.collectable_volume = tank.current_volume
    else:
        if (optimization_parameters.vehicle.capacity - cycle.cycle_volume) / tank.overflow_capacity >= optimization_parameters.constraints.percentage_volume_threshold:
            tank.collectable_volume = optimization_parameters.vehicle.capacity - cycle.cycle_volume
        else :
            tank.collectable_volume = 0
    
def update_return(cycle: Cycle, tank: Tank, optimization_parameters: OptimizationParameters):
    total_volume = cycle.cycle_volume + tank.collectable_volume
    manoever_time = total_volume / optimization_parameters.vehicle.draining_speed # chg
    tank.time_to_storehouse = ((calculate_distance(optimization_parameters.storehouse, tank) * 60) / optimization_parameters.vehicle.speed) * K
    tank.return_time = tank.time_to_storehouse + manoever_time + optimization_parameters.vehicle.loading_time

def try_reduce_collectable_volume(tank: Tank, excess_time: datetime, optimization_parameters: OptimizationParameters):
    new_volume = tank.collectable_volume - (excess_time * optimization_parameters.vehicle.pumping_speed)
    if new_volume / tank.overflow_capacity >= optimization_parameters.constraints.percentage_volume_threshold:
        tank.collectable_volume = new_volume
    else:
        None

def optim_swap(journey: Journey, tanks: List[Tank], pair: Tuple[Tank,Tank], optimization_parameters: OptimizationParameters):
    cycles_selected_tanks = get_cycles_tanks(journey=journey, pair=pair)
    new_journey = Journey(starting_time=journey.starting_time, ending_time=journey.ending_time, break_time=journey.break_time)
    tanks_copy = deepcopy(tanks)

    for i, cycle_selected_tanks in enumerate(cycles_selected_tanks):
        starting_time_cycle, ending_time_cycle = journey.cycles[i].starting_time, journey.cycles[i].ending_time
        new_cycle = Cycle(starting_time=starting_time_cycle, ending_time=ending_time_cycle)

        for selected_tank in cycle_selected_tanks:
            # print('tank courant', selected_tank.id)
            update_current_volume(selected_tank=selected_tank, tanks=tanks_copy)
            update_attributes(cycle=new_cycle, tank=selected_tank, optimization_parameters=optimization_parameters)
            update_return(cycle=new_cycle, tank=selected_tank, optimization_parameters=optimization_parameters)
            
            collect_time = selected_tank.time_to_go + selected_tank.collectable_volume / optimization_parameters.vehicle.pumping_speed + optimization_parameters.vehicle.loading_time
            predicted_ending_time = new_cycle.current_time + timedelta(minutes=collect_time + selected_tank.return_time)

            if not selected_tank.is_available(dt=new_cycle.current_time + timedelta(minutes=selected_tank.time_to_go)):
                # print('error availability')
                # print("arriving datetime =",new_cycle.current_time + timedelta(minutes=selected_tank.time_to_go))
                # print('hours =', selected_tank.maker.hours)
                return None
            
            elif not (new_cycle.ending_time >= predicted_ending_time):
                # print('error ending time')
                # print('predicted ending time',new_cycle.current_time + timedelta(minutes=collect_time + selected_tank.return_time))
                # print('ending time', new_cycle.ending_time

                excess_time = (predicted_ending_time - new_cycle.ending_time).total_seconds() / 60
                if try_reduce_collectable_volume(tank=selected_tank, excess_time=excess_time, optimization_parameters=optimization_parameters) is not None:
                    update_return(cycle=new_cycle, tank=selected_tank, optimization_parameters=optimization_parameters)
                    # print('adding_tank')
                    new_cycle.add_tank(choice=selected_tank, optimization_parameters=optimization_parameters)
                else :
                    return None
            else:
                # print('adding_tank')
                new_cycle.add_tank(choice=selected_tank, optimization_parameters=optimization_parameters)

        new_journey.add_cycle(cycle=new_cycle)
        new_journey.current_time += timedelta(minutes=new_cycle.cycle_time)
    return new_journey

def swap(journey: Journey, tanks: List[Tank], optimization_parameters: OptimizationParameters):
    tank_time = get_couples(journey=journey)
    possible_swaps = get_possible_swaps(tank_time=tank_time)
    new_journeys = []
    for i,pair in enumerate(possible_swaps):
        new_journey = optim_swap(journey=journey, tanks=tanks, pair=pair, optimization_parameters=optimization_parameters)
        if new_journey is not None:
            new_journeys.append(new_journey)

