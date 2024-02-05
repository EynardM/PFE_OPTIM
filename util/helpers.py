from util.imports import * 
from util.objects import *


def parse_config(filename: str):
    with open(filename, 'r') as file:
        config_data = json.load(file)

    optimization_parameters = Parameters(**config_data['optimization_parameters'])
    storehouse = Storehouse(**config_data['storehouse'])
    agent = Agent(**config_data['agent'])

    # print_colored(optimization_parameters, "yellow")
    # print_colored(storehouse, "cyan")
    # print_colored(agent, "magenta")

    return optimization_parameters, storehouse, agent

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

def filter_quantities(tanks : List[Tank], parameters: Parameters) -> List[Tank]:
    tanks_filtered_by_quantity = []
    for tank in tanks: 
        if tank.current_volume / tank.overflow_capacity >= parameters.percentage_volume_threshold:
            tanks_filtered_by_quantity.append(tank)
    return tanks_filtered_by_quantity

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_pareto_front_3d(algorithm_data):
    # Collecter les évaluations du front de Pareto
    evaluations = [data["evaluation"] for data in algorithm_data.values()]
    evaluations = np.array(evaluations)

    # Trier les évaluations par ordre lexicographique
    sorted_indices = np.lexsort((evaluations[:, 0], evaluations[:, 1], evaluations[:, 2]))
    sorted_evaluations = evaluations[sorted_indices]

    # Créer le graphique pour la tendance
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot de la tendance en reliant les points
    ax.plot(sorted_evaluations[:, 0], sorted_evaluations[:, 1], sorted_evaluations[:, 2], label='Trend', color='red')

    # Ajouter les points de chaque solution
    for name, data in algorithm_data.items():
        evaluation = data["evaluation"]
        ax.scatter(evaluation[0], evaluation[1], evaluation[2], label=name)

    # Ajouter les étiquettes des axes
    ax.set_xlabel('Total Volume')
    ax.set_ylabel('Total Distance')
    ax.set_zlabel('Maximum Emergency')

    # Afficher le graphique
    plt.title('Pareto Front 3D')
    ax.legend()
    plt.show()






