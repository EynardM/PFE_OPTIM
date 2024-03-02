from util.imports import * 
from util.objects import *
from util.locations import *
from util.common import *
from util.variables import *

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

def filter_days(tanks : List[Tank], delta_days: int) -> List[Tank]:
    now = datetime.now() - timedelta(days=delta_days)
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

def get_eval_weights(journeys: List[Journey]):
    max_volume = float('-inf')
    max_distance = float('-inf')
    max_emergency = float('-inf')

    for journey in journeys:
        if journey.journey_volume > max_volume:
            max_volume = journey.journey_volume
        
        if journey.journey_distance > max_distance:
            max_distance = journey.journey_distance
        
        if journey.journey_global_emergency > max_emergency:
            max_emergency = journey.journey_global_emergency

    weight_Q = alpha_Q/max_volume
    weight_D = alpha_D/max_distance
    weight_E = alpha_E/max_emergency

    return weight_Q, weight_D, weight_E
    
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

def plot_pareto_front(solutions, journey_id, FOLDER_PATH=NEIGHBORS_PARETO_FRONTS_PATH):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlabel('Volume')
    ax.set_ylabel('Distance')
    ax.set_zlabel('Emergency')
    plt.title('Pareto Front')

    # Filter Pareto front solutions
    pareto_front = get_pareto_front(solutions)

    # Create colormap for methods
    unique_methods = sorted(set(sol['method'] for sol in solutions))
    colormap = plt.cm.get_cmap('tab10', len(unique_methods))

    # Plot all solutions
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

    # Plot Pareto front layer if there are at least three points
    if len(pareto_front) > 3:
        pareto_front_volume = np.array([sol['volume'] for sol in pareto_front])
        pareto_front_distance = np.array([sol['distance'] for sol in pareto_front])
        pareto_front_emergency = np.array([sol['emergency'] for sol in pareto_front])
        ax.plot_trisurf(pareto_front_volume, pareto_front_distance, pareto_front_emergency, color='red', alpha=0.5)

    # Calculate percentage of each method in Pareto front
    method_percentage = {}
    for method in unique_methods:
        method_solutions = [sol for sol in pareto_front if sol['method'] == method]
        method_percentage[method] = len(method_solutions) / len(pareto_front) * 100

    # Create legend with method percentages
    legend_labels = [f"{method} ({method_percentage[method]:.2f}%)" for method in unique_methods]
    ax.legend(handles=scatter_handles, labels=legend_labels)

    # Save figure
    filename = os.path.join(FOLDER_PATH, f"journey_{journey_id}.png")
    plt.savefig(filename)
    plt.close('all')

def generate_box_plots(input_xlsx):
    # Lire le fichier Excel avec pandas
    xls = pd.ExcelFile(input_xlsx)

    # Boucler sur chaque feuille Excel
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(input_xlsx, sheet_name=sheet_name)

        # Créer le chemin complet du fichier de sortie
        output_filename = f"{sheet_name}.png"
        output_filepath = os.path.join(BOX_PLOTS_PATH, output_filename)

        # Générer le boxplot pour chaque colonne
        plt.figure(figsize=(10, 6))
        for i, column in enumerate(['Score', 'Volume', 'Distance', 'Emergency'], start=1):
            plt.subplot(2, 2, i)
            bp = df.boxplot(column=column, by='Method', ax=plt.gca())
            plt.title(f'Boxplot {column}')
            plt.xlabel('Method')
            plt.ylabel(column)
            plt.xticks(rotation=45)
            plt.xticks(range(1, len(df['Method'].unique()) + 1), sorted(df['Method'].unique()))

        plt.suptitle(f'Boxplots - {sheet_name}')
        plt.tight_layout()

        # Sauvegarder le boxplot dans le dossier de sortie
        plt.savefig(output_filepath)
        plt.close()

def get_results(solutions, delta_days: int, folder_path):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlabel('Volume')
    ax.set_ylabel('Distance')
    ax.set_zlabel('Emergency')
    plt.title('Pareto Front')

    # Filter Pareto front solutions
    pareto_front = get_pareto_front(solutions)

    # Create colormap for methods
    unique_methods = sorted(set(sol['method'] for sol in solutions))
    colormap = plt.cm.get_cmap('tab10', len(unique_methods))

    # Plot all solutions
    # Calculate method percentages in Pareto front
    method_percentages = {}
    total_pareto_count = len(pareto_front)
    for method_index, method in enumerate(unique_methods):
        method_solutions_in_pareto = [sol for sol in pareto_front if sol['method'] == method]
        method_pareto_count = len(method_solutions_in_pareto)
        method_percentages[method] = (method_pareto_count / total_pareto_count) * 100

    # Plot all solutions
    scatter_handles = []
    for method_index, method in enumerate(unique_methods):
        method_solutions = [sol for sol in solutions if sol['method'] == method]
        method_solutions_sorted = sorted(method_solutions, key=lambda x: x['score'], reverse=True)

        method_color = colormap(method_index / len(unique_methods))
        scatter_handle = ax.scatter([sol['volume'] for sol in method_solutions],
                                    [sol['distance'] for sol in method_solutions],
                                    [sol['emergency'] for sol in method_solutions],
                                    c=[method_color] * len(method_solutions),
                                    label=f"{method} ({method_percentages[method]:.2f}%)")
        scatter_handles.append(scatter_handle)

    # Plot Pareto front layer
    pareto_front_volume = np.array([sol['volume'] for sol in pareto_front])
    pareto_front_distance = np.array([sol['distance'] for sol in pareto_front])
    pareto_front_emergency = np.array([sol['emergency'] for sol in pareto_front])
    ax.plot_trisurf(pareto_front_volume, pareto_front_distance, pareto_front_emergency, color='red', alpha=0.5)

    ax.legend(handles=scatter_handles)
    plt.savefig(os.path.join(folder_path, f'pareto_front.png'))

    plt.close('all')

    # Initialize an empty DataFrame for values
    values_data = []

    # Append data to the list
    for method in unique_methods:
            method_solutions = [sol for sol in solutions if sol['method'] == method]
            method_solutions_sorted = sorted(method_solutions, key=lambda x: x['score'], reverse=True)
            for sol in method_solutions_sorted:
                values_data.append({'Method': method,
                                    'Score': sol['score'],
                                    'Volume': sol['volume'],
                                    'Distance': sol['distance'],
                                    'Emergency': sol['emergency']})

    # Create DataFrame from the list of dictionaries
    values_df = pd.DataFrame(values_data)

    # Save values to Excel with sheet name as day+str(delta_days)
    values_xlsx_path = os.path.join(folder_path, 'values.xlsx')
    if not os.path.isfile(values_xlsx_path):
        values_df.to_excel(values_xlsx_path, sheet_name=f'day{delta_days}', index=False)
    else:
        with pd.ExcelWriter(values_xlsx_path, engine='openpyxl', mode='a') as writer:
            values_df.to_excel(writer, sheet_name=f'day{delta_days}', index=False)

    # Calculate method percentages
    method_counts = {method: sum(1 for sol in pareto_front if sol['method'] == method) for method in unique_methods}
    total_solutions = len(pareto_front)
    percentages_data = [{'Method': method, 'Percentage': (count / total_solutions) * 100} for method, count in method_counts.items()]

    # Create DataFrame for method percentages
    percentages_df = pd.DataFrame(percentages_data)

    # Save percentages to Excel with sheet name as day+str(delta_days)
    percentages_xlsx_path = os.path.join(folder_path, 'percentages.xlsx')
    if not os.path.isfile(percentages_xlsx_path):
        percentages_df.to_excel(percentages_xlsx_path, sheet_name=f'day{delta_days}', index=False)
    else:
        with pd.ExcelWriter(percentages_xlsx_path, engine='openpyxl', mode='a') as writer:
            percentages_df.to_excel(writer, sheet_name=f'day{delta_days}', index=False)

    generate_box_plot(input_xlsx=os.path.join(folder_path, 'values.xlsx'), folder_path=folder_path)

def generate_progress_graph(progress_iter, progress_score, journey_id, itermax, folder_path):
    # Création des listes pour les itérations et les scores
    iterations = []
    scores = []

    # Parcours de toutes les itérations jusqu'à itermax
    for i in range(itermax):
        # Si l'itération courante est dans progress_iter
        if i in progress_iter:
            # Ajouter l'itération et son score correspondant
            index = progress_iter.index(i)
            iterations.append(i)
            scores.append(progress_score[index])
        # Si aucune itération n'a été ajoutée et qu'on n'a pas atteint itermax
        elif not iterations and i < itermax - 1:
            # Ajouter l'itération et le score initial
            iterations.append(i)
            scores.append(progress_score[0])

    # Si aucune itération n'a été ajoutée et qu'on a atteint itermax
    if not iterations:
        # Ajouter l'itération finale et le dernier score
        iterations.append(itermax - 1)
        scores.append(progress_score[-1])

    # Création du graphique
    plt.plot(iterations, scores)
    plt.xlabel('Iteration')
    plt.ylabel('Score')
    plt.title(f'Journey : {journey_id}')
    plt.savefig(os.path.join(folder_path, f'progress_journey_{journey_id}.png'))
    plt.close()

def save_results_to_path(results, folder_path):
    for index, result in enumerate(results, start=1):
        result_filename = os.path.join(folder_path, f"journey_{index}.pickle")
        with open(result_filename, "wb") as file:
            pickle.dump(result, file)

def save_solutions(journey_id, solutions):
    data = []

    for solution in solutions:
        data.append({
            "Method": solution["method"],
            "Score": solution["score"],
            "Volume": solution["volume"],
            "Distance": solution["distance"],
            "Emergency": solution["emergency"]
        })

    df = pd.DataFrame(data)
    
    if not os.path.exists(NEIGHBORS_SOLUTIONS_PATH):
        os.makedirs(NEIGHBORS_SOLUTIONS_PATH)

    df.to_excel(os.path.join(NEIGHBORS_SOLUTIONS_PATH, f"journey_{journey_id}.xlsx"), index=False)

def generate_box_plot(input_xlsx, folder_path, filename=None):
    if filename is not None:
        name = 'journey_'+filename.split('.')[0].split('_')[1]
    else:
        name = 'boxplot'
    df = pd.read_excel(input_xlsx)

    plt.figure(figsize=(10, 6))
    for i, column in enumerate(['Score', 'Volume', 'Distance', 'Emergency'], start=1):
        plt.subplot(2, 2, i)
        bp = df.boxplot(column=column, by='Method', ax=plt.gca())
        plt.title(f'Boxplot {column}')
        plt.xlabel('Method')
        plt.ylabel(column)
        plt.xticks(rotation=45)
        plt.xticks(range(1, len(df['Method'].unique()) + 1), sorted(df['Method'].unique()))

    plt.suptitle('')
    plt.tight_layout()
    plt.savefig(os.path.join(folder_path, f"{name}.png"))
    plt.close()

def get_journeys(folder_path):
    results_dict = {}
    for file in os.listdir(folder_path):
        if file.endswith(".pickle"):
            chemin_file = os.path.join(folder_path, file)
            
            with open(chemin_file, "rb") as f:
                pickle_objects = pickle.load(f)
            pickle_objects
            filename = file.split('.')[0]
            if filename not in results_dict:
                results_dict[filename] = []

            for journey in pickle_objects:
                results_dict[filename].append(journey) 
                
    return results_dict

def plot_comp_optim_methods(tanks: List[Tank], basic_journeys: List[Journey], filename="evolution_scores_optim.png"):

    hill_climbing_results = get_journeys(folder_path=HILL_CLIMBING_PICKLES_LOWER_COMPLEXITY_PATH)
    simulated_annealing_results = get_journeys(folder_path=SIMULATED_ANNEALING_PICKLES_PATH)

    best_scores_hc = [journey[-1].evaluation(tanks=tanks) for key, journey in hill_climbing_results.items()]
    best_scores_sa = [journey[-1].evaluation(tanks=tanks) for key, journey in simulated_annealing_results.items()]
    scores_basic = [journey.evaluation(tanks=tanks) for journey in basic_journeys]

    x_values = list(range(1, len(hill_climbing_results.keys()) + 1))

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x_values, y=best_scores_hc,
                        mode='lines',
                        line=dict(color='green', width=1),
                        name='Hill Climbing'))

    fig.add_trace(go.Scatter(x=x_values, y=best_scores_sa,
                        mode='lines',
                        line=dict(color='red', width=1),
                        name='Simulated Annealing'))
    
    fig.add_trace(go.Scatter(x=x_values, y=scores_basic,
                        mode='lines',
                        line=dict(color='blue', width=1),
                        name='Base'))

    fig.update_layout(title='Scores des méthodes d\'optimisation',
                    xaxis_title='Voyage ID',
                    yaxis_title='Score',
                    legend=dict(orientation='h'),
                    margin=dict(l=50, r=50, t=50, b=50))

    filepath = os.path.join(OPTIM_RESULTS_PATH, filename)
    fig.write_image(filepath)