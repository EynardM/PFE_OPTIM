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
    if method == "HQDE":
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

def plot_pareto_front_3d(solutions, filename="pareto_front_plot.png"):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlabel('Volume')
    ax.set_ylabel('Distance')
    ax.set_zlabel('Emergency')
    plt.title('Pareto Front 3D')

    # Filtrer les solutions du front de Pareto
    pareto_front = get_pareto_front(solutions)

    # Créer une carte de couleur (colormap) pour les méthodes
    unique_methods = sorted(set(sol['method'] for sol in solutions))
    colormap = plt.cm.get_cmap('tab10', len(unique_methods))

    # Tracer toutes les solutions
    scatter_handles = []
    for method_index, method in enumerate(unique_methods):
        method_solutions = [sol for sol in solutions if sol['method'] == method]
        method_solutions_sorted = sorted(method_solutions, key=lambda x: x['score'], reverse=True)

        method_color = colormap(method_index / len(unique_methods))
        scatter_handle = ax.scatter([sol['volume'] for sol in method_solutions],
                                    [sol['distance'] for sol in method_solutions],
                                    [sol['emergency'] for sol in method_solutions],
                                    c=[method_color] * len(method_solutions),
                                    label=method)
        scatter_handles.append(scatter_handle)
        print(f"Meilleures solutions pour la méthode {method}:")
        for sol in method_solutions_sorted[:3]:
            print(f"Score: {sol['score']}, Volume: {sol['volume']}, Distance: {sol['distance']}, Emergency: {sol['emergency']}")

    # Tracer une couche pour le front de Pareto
    pareto_front_volume = np.array([sol['volume'] for sol in pareto_front])
    pareto_front_distance = np.array([sol['distance'] for sol in pareto_front])
    pareto_front_emergency = np.array([sol['emergency'] for sol in pareto_front])
    ax.plot_trisurf(pareto_front_volume, pareto_front_distance, pareto_front_emergency, color='red', alpha=0.5)

    method_counts = {method: sum(1 for sol in pareto_front if sol['method'] == method) for method in unique_methods}
    total_solutions = len(pareto_front)
    for method, count in method_counts.items():
        percentage = (count / total_solutions) * 100
        print(f"Méthode {method}: {percentage:.2f}%")

    # Ajouter une légende
    ax.legend(handles=scatter_handles)

    plt.savefig(filename)
    plt.show()
    return pareto_front

def get_pareto_front(solutions):
    pareto_front = []
    for sol in solutions:
        is_pareto = True
        for other in solutions:
            if (other['volume'] > sol['volume'] and other['distance'] <= sol['distance'] and other['emergency'] <= sol['emergency']) or \
               (other['volume'] >= sol['volume'] and other['distance'] < sol['distance'] and other['emergency'] <= sol['emergency']) or \
               (other['volume'] >= sol['volume'] and other['distance'] <= sol['distance'] and other['emergency'] < sol['emergency']):
                is_pareto = False
                break
        if is_pareto:
            pareto_front.append(sol)
    return pareto_front

def is_available(starting_time: datetime, cycle: Cycle, choice: Tank, storehouse: Storehouse, parameters: Parameters):
    last_point = cycle.get_last_point(storehouse=storehouse)
    time_to_go = ((calculate_distance(last_point, choice) * 60) / parameters.vehicle_speed) * K
    ending_time = starting_time + timedelta(minutes=time_to_go)
    if choice.is_available(dt=ending_time):
        return True
    return False

def get_random_position(cycles_positions):
    # Filtrer les sous-listes non vides
    cycles_positions_tmp = [(index, cycle_position) for index, cycle_position in enumerate(cycles_positions) if cycle_position]

    if cycles_positions_tmp:
        # Choisir une sous-liste non vide au hasard
        index, cycle_position_tmp = random.choice(cycles_positions_tmp)

        # Choisir une position aléatoire à l'intérieur de la sous-liste sélectionnée
        position = random.choice(cycle_position_tmp)

        return index, position
    else:
        return None

def check_choice(journey: Journey, choice: Tank, cycle: Cycle, cycles: List[Cycle], storehouse: Storehouse, parameters: Parameters) -> Tank:
    # Time to go 
    last_point = cycle.get_last_point(storehouse=storehouse)
    choice.time_to_go = ((calculate_distance(last_point, choice) * 60) / parameters.vehicle_speed) * K
    colored(choice.time_to_go, "cyan", "choice.time_to_go")

    # Collectable volume 
    if choice.current_volume <= parameters.mobile_tank_volume - cycle.cycle_volume:
            choice.collectable_volume = choice.current_volume
    else:
            if (parameters.mobile_tank_volume - cycle.cycle_volume) / choice.overflow_capacity >= parameters.percentage_partial_collect_volume:
                choice.collectable_volume = parameters.mobile_tank_volume - cycle.cycle_volume
            else :
                choice.collectable_volume = 0
    colored(choice.collectable_volume, "cyan", "choice.collectable_volume")

    # Manoever time
    choice.manoever_time = choice.collectable_volume / parameters.pumping_speed
    total_collect_time = choice.time_to_go + choice.manoever_time + parameters.loading_time
    colored(total_collect_time, "cyan")

    # Time to return 
    choice.time_to_storehouse = ((calculate_distance(choice, storehouse) * 60) / parameters.vehicle_speed) * K
    colored(choice.time_to_storehouse, "cyan", "choice.time_to_storehouse")

    # Return time
    choice.return_time = choice.time_to_storehouse + ((cycle.cycle_volume + choice.collectable_volume) / parameters.draining_speed) + parameters.loading_time
    colored(choice.return_time, "cyan", "choice.return_time")

    # Check remaining_time
    actual_journey_time = sum([cycle.cycle_time for cycle in cycles])

    remaining_time = (journey.end_time.hour - journey.start_time.hour)*60 - actual_journey_time
    colored(remaining_time, "yellow")
    yey = (cycle.cycle_time + total_collect_time + choice.return_time)
    colored(yey, "red")
    colored(cycle.cycle_time, "blue", "cycle.cycle_time")
    if remaining_time - (cycle.cycle_time + total_collect_time + choice.return_time) > 0:
        return True
    else :
        return False
 
def permutation(journey: Journey, tanks : List[Tank], storehouse: Storehouse, parameters: Parameters):
    unused_tanks = [tank for tank in tanks]
    for cycle in journey.cycles:
        for tank_cycle in cycle.selected_tanks:
            for tank in unused_tanks:
                if tank.id == tank_cycle.id : 
                    unused_tanks.remove(tank)

    # Choix du tank à rajouter
    choice = random.choice(unused_tanks)
    colored(choice, "yellow")
    colored(choice.maker.hours, "magenta", "hours")
    
    # Parcours les cuves de chaque cycle et tester si la cuve choisie est atteignable depuis la cuve en cours
    cycles_positions = []
    cycles = []
    for cycle in journey.cycles:
        cycle_positions = []
        current_time = cycle.starting_time
        if is_available(starting_time=current_time, cycle=cycle, choice=choice, storehouse=storehouse, parameters=parameters):
            cycle_positions.append(-1)
        for i in range(len(cycle.selected_tanks)):
            current_time += timedelta(minutes=cycle.travel_times[i]+cycle.manoever_times[i]+parameters.loading_time)
            if is_available(starting_time=current_time, cycle=cycle, choice=choice, storehouse=storehouse, parameters=parameters):
                cycle_positions.append(i)
        cycles_positions.append(cycle_positions)
    
    # Choisir un index où ajouter la louloutte
    cycle_index, choice_position = get_random_position(cycles_positions)

    # Relancer un algo
    """for i,cycle in enumerate(journey.cycles):
        if i != index_sublist:
            cycles.append(cycle)
        else :
            new_cycle = Cycle(starting_time=cycle.starting_time)
            if position == -1:
                if check_choice(journey=journey, choice=choice, cycle=new_cycle, cycles=cycles, storehouse=storehouse, parameters=parameters):
                        new_cycle.add_tank(choice=choice, parameters=parameters)
                        break
            else :
                for j,tank in enumerate(cycle.selected_tanks):
                    if j-1 == position:
                        if check_choice(journey=journey, choice=choice, cycle=new_cycle, cycles=cycles, storehouse=storehouse, parameters=parameters):
                                print(f"added, j = {j}, position = {position}")
                                new_cycle.add_tank(choice=choice, parameters=parameters)
                                break
                    else :
                        new_cycle.add_tank(choice=tank, parameters=parameters) """

    return cycle_index, choice_position, choice