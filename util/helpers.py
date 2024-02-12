from util.imports import * 
from util.objects import *
             
def parse_config(filename: str) -> tuple:
    with open(filename, 'r') as file:
        config_data = json.load(file)

    constraints_data = config_data['constraints']
    vehicle_data = config_data['vehicule']
    storehouse_data = config_data['storehouse']
    agent_data = config_data['agent']

    constraints = Constraints(**constraints_data)
    vehicle = Vehicle(**vehicle_data)
    storehouse = Storehouse(**storehouse_data)
    agent = Agent(**agent_data)

    return constraints, vehicle, storehouse, agent

def create_maker_objects_from_dataframe(df):
    makers_list = []
    for index, row in df.iterrows():
        maker = Maker(
            row['keys_tanks'],
            row['collector'],
            row['ending_vacation'],
            row['days'],
            row['opening_vacation'],
            row['address'],
            row['hours'],
            row['country'],
            row['name'],
            row['post_code'],
            row['city'],
            row['internal_name'],
            row['longitude'],
            row['id'],
            row['latitude']
        )
        makers_list.append(maker)
    return makers_list

def create_tank_objects_from_dataframe(df):
    tanks_list = []
    for index, row in df.iterrows():
        tank = Tank(
            row['barcode'],
            row['collector'],
            row['overflow_capacity'],
            row['last_reading_date'],
            row['tank_type_label'],
            row['tank_type_id'],
            row['nominal_capacity'],
            row['container_type_label'],
            row['tank_name'],
            row['key_maker'],
            row['container_type_id'],
            row['tank_status_label'],
            row['current_volume'],
            row['id'],
            row['tank_status_id'],
            row['fill_level']
        )
        tanks_list.append(tank)
    return tanks_list

def create_measurement_objects_from_dataframe(df):
    measurement_list = []
    for index, row in df.iterrows():
        measurement = Measurement(
            row['id'],
            row['drainage'],
            row['event_type_id'],
            row['event_type_label'],
            row['fill_level'],
            row['filling'],
            row['key_maker'],
            row['key_tank'],
            row['measured_height'],
            row['measurement_date'],
            row['measurement_status_id'],
            row['measurement_status_label'],
            row['note_type_id'],
            row['note_type_label'],
            row['vidange'],
            row['volume']
        )
        measurement_list.append(measurement)
    return measurement_list

def filter_days(tanks : List[Tank]) -> List[Tank]:
    now = datetime.now()
    day = now.strftime("%A")
    day_index = {calendar.day_name[i]: i for i in range(7)}[day]

    tanks_filtered_by_days = []
    for tank in tanks:
        if tank.maker.days[day_index] == 1:
            tanks_filtered_by_days.append(tank)
    return tanks_filtered_by_days

def filter_quantities(tanks : List[Tank], constraints: Constraints) -> List[Tank]:
    tanks_filtered_by_quantity = []
    for tank in tanks: 
        if tank.current_volume / tank.overflow_capacity >= constraints.percentage_volume_threshold:
            tanks_filtered_by_quantity.append(tank)
    return tanks_filtered_by_quantity

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