from util.imports import * 
from util.objects import *
from util.variables import *
from util.helpers import *

def count_total_elements(lst):
    total_elements = 0
    for item in lst:
        if isinstance(item, list) or isinstance(item, tuple) :
            total_elements += count_total_elements(item)  
        else:
            total_elements += 1 
    return total_elements

def generate_time_slots(tanks: List[Tank], parameters: Parameters, agent: Agent):
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
    while current_time + timedelta(hours=parameters.working_time) <= end:
        end_time = current_time + timedelta(hours=parameters.working_time)
        time_slots_without_break.append(((current_time, end_time)))
        current_time += timedelta(hours=1)

    # Generate working slots with break
    time_slots = []
    current_time = start
    while current_time + timedelta(hours=parameters.working_time+ BREAK_TIME) <= end:
        end_time = current_time + timedelta(hours=parameters.working_time+ BREAK_TIME)
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
                time_slots_with_break.append(((time_slot[0], new_start), (new_end, time_slot[1])) )
    
    return time_slots_without_break, time_slots_with_break
              
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

def get_available_tanks(starting_time: datetime, cycle: Cycle, tanks: List[Tank], storehouse: Storehouse, parameters: Parameters) -> List[Tank]:
    last_point = cycle.get_last_point(storehouse=storehouse)
    available_tanks = []
    for tank in tanks: 
        # print(f"lat1, lon1 {last_point.get_coordinates()}, lat2, lon2 {tank.get_coordinates()}, dist = {dist}")
        tank.time_to_go = ((calculate_distance(last_point, tank) * 60) / parameters.vehicle_speed) * K
        # print(tank.time_to_go)
        ending_time = starting_time + timedelta(minutes=tank.time_to_go)
        if tank.is_available(dt=ending_time):
            available_tanks.append(tank)
    return available_tanks

def get_valid_choices(tanks: List[Tank], cycle: Cycle, parameters: Parameters) -> List[Tank]:
    valid_tanks = []  
    for tank in tanks:
        if tank.current_volume <= parameters.mobile_tank_volume - cycle.cycle_volume:
            tank.collectable_volume = tank.current_volume
            valid_tanks.append(tank)
        else:
            if (parameters.mobile_tank_volume - cycle.cycle_volume) / tank.overflow_capacity >= parameters.percentage_partial_collect_volume:
                tank.collectable_volume = parameters.mobile_tank_volume - cycle.cycle_volume
                valid_tanks.append(tank)
    return valid_tanks

def check_storehouse_return(journey: Journey, tanks: List[Tank], cycle: Cycle, storehouse: Storehouse, parameters: Parameters) -> List[Tank]:
    final_candidates = []
    for tank in tanks:
        tank.manoever_time = tank.collectable_volume / parameters.pumping_speed
        total_collect_time = tank.time_to_go + tank.manoever_time + parameters.loading_time
        tank.time_to_storehouse = ((calculate_distance(tank, storehouse) * 60) / parameters.vehicle_speed) * K
        tank.return_time = tank.time_to_storehouse + ((cycle.cycle_volume + tank.collectable_volume) / parameters.draining_speed) + parameters.loading_time
        remaining_time = (journey.end_time.hour - journey.start_time.hour)*60 - journey.journey_time
        if remaining_time - (cycle.cycle_time + total_collect_time + tank.return_time) > 0:
            final_candidates.append(tank)
    return final_candidates
        
def choice_function(starting_point: Union[Tank, Storehouse], tanks: List[Tank], method):
    methods = ["R", "Q", "D", "E", "HQD", "HQDE"]

    if method == "Random":
        method = random.choice(methods)

    elif method == "R":
        tank_chosen = random.choice(tanks)
    elif method == "Q":
        tank_chosen = max(tanks, key=lambda tank: tank.collectable_volume)
    elif method == "D":
        tank_chosen = min(tanks, key=lambda tank: calculate_distance(starting_point, tank))
    elif method == "E":
        tank_chosen = max(tanks, key=lambda tank: (tank.current_volume / tank.overflow_capacity))
    elif method == "HQD":
        scores = [weight_Q*tank.collectable_volume + weight_D*(calculate_distance(starting_point, tank)) for tank in tanks]
        tank_chosen  = tanks[max(range(len(scores)), key=lambda i: scores[i])]
    elif method == "HQDE":
        scores = [weight_Q*tank.collectable_volume + weight_D*(calculate_distance(starting_point, tank)) + weight_E*(tank.current_volume/tank.overflow_capacity) for tank in tanks]
        tank_chosen  = tanks[max(range(len(scores)), key=lambda i: scores[i])]
    
    return tank_chosen

def concatenate_journeys(journeys: List[Journey]) -> Journey:
    # Sort the list of journeys by start time
    sorted_journeys = sorted(journeys, key=lambda x: x.start_time)

    # Determine start_time and end_time for the concatenated journey
    start_time = sorted_journeys[0].start_time
    end_time = sorted_journeys[-1].end_time

    # Initialize concatenated journey attributes
    concatenated_journey = Journey(start_time, end_time)
    concatenated_journey.journey_time = sum(journey.journey_time for journey in sorted_journeys)
    concatenated_journey.journey_volume = sum(journey.journey_volume for journey in sorted_journeys)
    concatenated_journey.journey_distance = sum(journey.journey_distance for journey in sorted_journeys)

    # Calculate break_time if needed
    break_times = []
    for i in range(len(sorted_journeys) - 1):
        if sorted_journeys[i].end_time < sorted_journeys[i + 1].start_time:
            break_times.append(sorted_journeys[i + 1].start_time - sorted_journeys[i].end_time)
    if break_times:
        concatenated_journey.break_time = sum(break_times, timedelta())

    # Concatenate cycles
    for journey in sorted_journeys:
        concatenated_journey.cycles.extend(journey.cycles)

    return concatenated_journey

def get_tank_from_list(tanks: List[Tank], tank_cycle: Tank):
    for tank in tanks:
        if tank_cycle.id == tank.id:
            return tank  
        
def verify_journey(journey: Journey, tanks:List[Tank], parameters: Parameters, storehouse: Storehouse):
    for cycle in journey.cycles:
        start_datetime = cycle.starting_time
        end_datetime = deepcopy(start_datetime)
        cycle_volume = 0 
        last_point = storehouse

        for i,tank_cycle in enumerate(cycle.selected_tanks):
            tank = get_tank_from_list(tanks=tanks, tank_cycle=tank_cycle)                
            travel_time = ((calculate_distance(last_point, tank) * 60) / parameters.vehicle_speed) * K

            # Checking if the travel time is the same
            if not travel_time == cycle.travel_times[i]:
                print(travel_time, cycle.travel_times[i])
                print("false travel time")
                return False
            
            # Checking if the tank is available (constraint hours)
            if not tank.is_available(dt=end_datetime+timedelta(minutes=travel_time)):
                print("false available")
                return False
            
            # Recalculate the volume to be taken from the tank
            if tank.current_volume <= parameters.mobile_tank_volume - cycle_volume: 
                collected_volume = tank.current_volume
            else:
                if (parameters.mobile_tank_volume - cycle_volume) / tank.overflow_capacity >= parameters.percentage_partial_collect_volume:
                    collected_volume = parameters.mobile_tank_volume - cycle_volume
                
            manoever_time = collected_volume / parameters.pumping_speed

            # Checking if the manoever time is the same
            if not manoever_time == cycle.manoever_times[i]:
                print("false manoever time")
                return False
            
            collect_time = travel_time + manoever_time + parameters.loading_time
            end_datetime += timedelta(minutes=collect_time)
            cycle_volume += collected_volume 
            last_point = tank_cycle

        # Back to storehouse
        return_time = ((calculate_distance(last_point, storehouse) * 60) / parameters.vehicle_speed) * K + cycle_volume / parameters.draining_speed + parameters.loading_time
        end_datetime += timedelta(minutes=return_time)

        # Checking if the end times are the same
        if not deepcopy(end_datetime).replace(microsecond=0) == deepcopy(cycle.ending_time).replace(microsecond=0):
            print("false ending_time")
            print(end_datetime)
            print(cycle.ending_time)
            return False
        
        # Checking if the volumes are the same and if it fits the constraint of the capacity of the mobile volume
        if not cycle_volume == cycle.cycle_volume and cycle_volume >= parameters.mobile_tank_volume:
            print("false volume")
            return False
    return True

def plot_pareto_front_3d(method_scores):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot chaque point de la couleur de la méthode auquel il correspond
    for method, scores in method_scores.items():
        scores_array = np.array([(score["volume"], score["distance"], score["emergency"]) for score in scores])
        ax.scatter(scores_array[:, 0], scores_array[:, 1], -scores_array[:, 2], label=method)

    ax.set_xlabel('Volume')
    ax.set_ylabel('Distance')
    ax.set_zlabel('Emergency')
    plt.title('Pareto Front 3D')
    ax.legend()
    plt.show()