from util.imports import *
from util.locations import *
from util.helpers import *
from util.objects import *
from util.decorator import *
from util.datamodule import *

from algorithms.helpers import *
from algorithms.run import *

from optim.neighbors import *

@timeit
def get_basic_journeys(tanks: List[Tank], delta_days: int):
    """
    Generate basic journeys based on optimization parameters and tank data.

    Args:
        tanks (List[Tank]): List of Tank objects.
        delta_days (int): Number of days for which journeys need to be generated.

    Returns:
        Tuple[List[Dict], List[Journey], List[OptimizationParameters]]:
            A tuple containing lists of dictionaries representing solutions,
            Journey objects representing generated journeys, and
            OptimizationParameters objects representing optimization parameters.
    """
    # Retrieve configuration parameters
    constraints, vehicle, storehouse, agent = parse_config('config.json')

    # Filter tanks based on open days
    tanks = filter_days(tanks=tanks, delta_days=delta_days)

    # Filter tanks based on quantity constraints
    tanks = filter_quantities(tanks=tanks, constraints=constraints)

    # Generate time slots for journeys
    time_slots = generate_time_slots(tanks=tanks, constraints=constraints, agent=agent)

    # Initialize lists for storing generated data
    journeys = []
    solutions = []
    parameters = []
    visited_journeys = {}

    # Generate optimization parameters for each combination of tanks and time slots
    optimization_parameters_list = generate_optimization_paremeters(tanks=tanks, constraints=constraints,
                                                                    vehicle=vehicle, storehouse=storehouse,
                                                                    agent=agent, time_slots=time_slots)
    # Generate journeys for each set of optimization parameters
    for optimization_parameters in optimization_parameters_list:
        journey = run(optimization_parameters=optimization_parameters)

        # Check if the generated journey is unique for this method
        if optimization_parameters.method in visited_journeys:
            found_match = False
            for journey_visited in visited_journeys[optimization_parameters.method]:
                if journey_visited.journey_time == journey.journey_time:
                    found_match = True
                    break

            if found_match:
                continue
            else:
                visited_journeys[optimization_parameters.method].append(journey)
        else:
            visited_journeys[optimization_parameters.method] = [journey]

        # Append generated journey, parameters, and evaluation score to respective lists
        journeys.append(journey)
        parameters.append(optimization_parameters)
        score = journey.evaluation(tanks=tanks)
        solutions.append({"method": optimization_parameters.method, "score": score,
                           "volume": journey.journey_volume, "distance": journey.journey_distance,
                           "emergency": journey.journey_global_emergency})

    # Save generated solutions to file system
    make_empty(folder=CURRENT_RESULTS_PATH)
    get_results(solutions=solutions, delta_days=delta_days, folder_path=CURRENT_RESULTS_PATH)
    return solutions, journeys, parameters

@timeit
def hill_climbing(journey: Journey, tanks: List[Tank], optimization_parameters: OptimizationParameters,
                  maximum_complexity: bool, journey_id: int) -> List[Journey]:
    """
    Perform hill climbing optimization algorithm to find the best journey.

    Args:
        journey (Journey): The initial journey to start optimization from.
        tanks (List[Tank]): List of Tank objects.
        optimization_parameters (OptimizationParameters): Optimization parameters.
        maximum_complexity (bool): Flag indicating whether to run with maximum complexity or not.
        journey_id (int): Identifier for the journey.

    Returns:
        List[Journey]: List of Journey objects representing the best journeys found during optimization.
    """
    tqdm.write('Launching hill climbing ...')
    best_journeys = [journey]

    if maximum_complexity:
        iter = 0
        progress = True
        progress_score = [journey.evaluation(tanks=tanks)]
        progress_iter = [iter]
        while(progress):
            best_journey = best_journeys[-1]
            new_journeys = get_neighbors(best_journey=best_journey, tanks=tanks,
                                         optimization_parameters=optimization_parameters,
                                         maximum_complexity=maximum_complexity)
            progress = False
            for new_journey in new_journeys:
                if new_journey.evaluation(tanks=tanks) >= best_journey.evaluation(tanks=tanks):
                    progress = True
                    best_journey = new_journey
                    best_journeys.append(best_journey)
                    progress_score.append(best_journey.evaluation(tanks=tanks))
                    progress_iter.append(iter+1)
            if progress:
                tqdm.write(f'Progress at iter {iter}')
            iter += 1
        tqdm.write('Hill climbing finished.')
        generate_progress_graph(progress_iter=progress_iter, progress_score=progress_score,
                        journey_id=journey_id, itermax=progress_iter[-1],
                        folder_path=HILL_CLIMBING_PROGRESS_MAXIMUM_COMPLEXITY_PATH)

    else:
        progress_score = [journey.evaluation(tanks=tanks)]
        progress_iter = [0]
        with tqdm(total=ITERMAX_HC) as pbar:
            for iter in range(ITERMAX_HC):
                best_journey = best_journeys[-1]
                new_journeys = get_neighbors(best_journey=best_journey, tanks=tanks,
                                             optimization_parameters=optimization_parameters,
                                             maximum_complexity=maximum_complexity)
                new_journey = random.choice(new_journeys)
                if new_journey.evaluation(tanks=tanks) >= best_journey.evaluation(tanks=tanks):
                    best_journey = new_journey
                    best_journeys.append(best_journey)
                    progress_score.append(best_journey.evaluation(tanks=tanks))
                    progress_iter.append(iter+1)
                pbar.update(1)
        generate_progress_graph(progress_iter=progress_iter, progress_score=progress_score,
                                journey_id=journey_id, itermax=ITERMAX_HC,
                                folder_path=HILL_CLIMBING_PROGRESS_LOWER_COMPLEXITY_PATH)
        tqdm.write('Hill climbing finished.')
    return best_journeys

@timeit
def simulated_annealing(initial_solution, tanks: List[Tank], optimization_parameters: OptimizationParameters,
                        maximum_complexity: bool, journey_id: int):
    """
    Perform simulated annealing optimization algorithm to find the best solution.

    Args:
        initial_solution (Journey): The initial solution to start optimization from.
        tanks (List[Tank]): List of Tank objects.
        optimization_parameters (OptimizationParameters): Optimization parameters.
        maximum_complexity (bool): Flag indicating whether to run with maximum complexity or not.
        journey_id (int): Identifier for the journey.

    Returns:
        List[Journey]: List of Journey objects representing the best solutions found during optimization.
    """
    tqdm.write('Launching simulated annealing ...')
    current_solution = initial_solution
    current_energy = current_solution.evaluation(tanks=tanks)
    
    best_solutions = [current_solution]   
    best_energy = current_energy

    temperature = INITIAL_TEMPERATURE

    progress_score = [best_energy]
    progress_iter = [0]
    with tqdm(total=ITERMAX_SA) as pbar:
        for iter in range(ITERMAX_SA):  
            current_solution = best_solutions[-1]
            neighbors = get_neighbors(best_journey=current_solution, tanks=tanks,
                                      optimization_parameters=optimization_parameters,
                                      maximum_complexity=maximum_complexity)
            
            next_solution = random.choice(neighbors)
            next_energy = next_solution.evaluation(tanks=tanks)

            energy_delta = next_energy - current_energy

            if energy_delta > 0 or random.uniform(0, 1) < math.exp(energy_delta / temperature):
                current_solution = next_solution
                current_energy = next_energy

                if current_energy > best_energy:
                    best_energy = current_energy
                    best_solutions.append(current_solution)
                    progress_score.append(current_solution.evaluation(tanks=tanks))
                    progress_iter.append(iter+1)

            temperature *= COOLING_RATE
            if temperature < MINIMAL_TEMPERATURE:
                break

            pbar.update(1)
    tqdm.write('Simulated annealing finished.')
    generate_progress_graph(progress_iter=progress_iter, progress_score=progress_score,
                            journey_id=journey_id, itermax=ITERMAX_SA,
                            folder_path=SIMULATED_ANNEALING_PROGRESS_PATH)
    return best_solutions

@timeit
def main(lower_complexity, maximum_complexity, example):
    """
    Main function to execute optimization algorithms.

    Args:
        maximum_complexity (bool): Flag indicating whether to run with maximum complexity or not.
    """
    measurements, tanks, makers = get_data()

    solutions, journeys, parameters = get_basic_journeys(tanks=tanks, delta_days=1)
    plot_comp_optim_methods(tanks=tanks, basic_journeys=journeys) # use this function to compare optimisation methods if pickles are saved already from a past run
    # print(get_eval_weights(journeys)) # to get the weights to be putted in "util/variables.py", use this line once before using any flag
    
    if example:
        make_empty(folder=NEIGHBORS_SOLUTIONS_PATH)
        make_empty(folder=NEIGHBORS_PARETO_FRONTS_PATH)
        make_empty(folder=NEIGHBORS_BOX_PLOTS_PATH)
        for i in range(example):
            print(f'\n#---------- Example : Journey n°{i}/{example} ----------#\n')
            journey = journeys[i]
            parameter = parameters[i]

            print(f'Generating neighbors with all techniques (permutation, swap, transfer) ...')
            permutation_journeys, swap_journeys, transfer_journeys = get_neighbors(best_journey=journey, tanks=tanks, 
                                                                                optimization_parameters=parameter,
                                                                                    maximum_complexity=True, example=True)
            print(f'Calculating solutions ...')
            solutions = []
            solutions.append({"method": "Base", "score": journey.evaluation(tanks=tanks),
                "volume": journey.journey_volume, "distance": journey.journey_distance,
                "emergency": journey.journey_global_emergency})
            
            for journey in permutation_journeys:
                solutions.append({"method": "Permutation", "score": journey.evaluation(tanks=tanks),
                            "volume": journey.journey_volume, "distance": journey.journey_distance,
                            "emergency": journey.journey_global_emergency})
            
            for journey in swap_journeys:
                solutions.append({"method": "Swap", "score": journey.evaluation(tanks=tanks),
                            "volume": journey.journey_volume, "distance": journey.journey_distance,
                            "emergency": journey.journey_global_emergency})
                
            for journey in transfer_journeys:
                solutions.append({"method": "Transfer", "score": journey.evaluation(tanks=tanks),
                            "volume": journey.journey_volume, "distance": journey.journey_distance,
                            "emergency": journey.journey_global_emergency})

            
            save_solutions(journey_id=i, solutions=solutions)
            plot_pareto_front(solutions=solutions, journey_id=i)
            print('Results saved.')

        for filename in os.listdir(NEIGHBORS_SOLUTIONS_PATH):
            if filename.endswith('.xlsx'):
                generate_box_plot(os.path.join(NEIGHBORS_SOLUTIONS_PATH, filename), NEIGHBORS_BOX_PLOTS_PATH, filename)
        print('\nBox plots saved.')

    if maximum_complexity:
        hill_climbing_results = []
        for i in range(maximum_complexity):
            print(f'\n#---------- Maximum complexity : Journey n°{i}/{maximum_complexity} ----------#\n')
            journey = journeys[i]
            parameter = parameters[i]
            hill_climbing_journeys = hill_climbing(journey=journey, tanks=tanks, optimization_parameters=parameter,
                                                maximum_complexity=True, journey_id=i)
            hill_climbing_results.append(hill_climbing_journeys)
        save_results_to_path(results=hill_climbing_results, folder_path=HILL_CLIMBING_PICKLES_MAXIMUM_COMPLEXITY_PATH)
    # if lower_complexity:
    #     hill_climbing_results = []
    #     simulated_annealing_results = []
    #     for i in range(lower_complexity):
    #         print(f'\n#---------- Lower complexity : Journey n°{i}/{lower_complexity} ----------#\n')
    #         journey = journeys[i]
    #         parameter = parameters[i]
            
    #         hill_climbing_journeys = hill_climbing(journey=journey, tanks=tanks, optimization_parameters=parameter,
    #                                             maximum_complexity=False, journey_id=i)
            
    #         simulated_annealing_journeys = simulated_annealing(initial_solution=journey, tanks=tanks,
    #                                                         optimization_parameters=parameter,
    #                                                         maximum_complexity=False, journey_id=i)
            
    #         hill_climbing_results.append(hill_climbing_journeys)
    #         simulated_annealing_results.append(simulated_annealing_journeys)

    #     save_results_to_path(results=hill_climbing_results, folder_path=HILL_CLIMBING_PICKLES_LOWER_COMPLEXITY_PATH)
    #     save_results_to_path(results=simulated_annealing_results, folder_path=SIMULATED_ANNEALING_PICKLES_PATH)
            
    hill_climbing_results = []
    simulated_annealing_results = []
    for i in range(len(journeys)):
        print(f'\n#---------- Lower complexity : Journey n°{i}/{lower_complexity} ----------#\n')
        journey = journeys[i]
        parameter = parameters[i]
        
        hill_climbing_journeys = hill_climbing(journey=journey, tanks=tanks, optimization_parameters=parameter,
                                            maximum_complexity=False, journey_id=i)
        
        simulated_annealing_journeys = simulated_annealing(initial_solution=journey, tanks=tanks,
                                                        optimization_parameters=parameter,
                                                        maximum_complexity=False, journey_id=i)
        
        hill_climbing_results.append(hill_climbing_journeys)
        simulated_annealing_results.append(simulated_annealing_journeys)

    save_results_to_path(results=hill_climbing_results, folder_path=HILL_CLIMBING_PICKLES_LOWER_COMPLEXITY_PATH)
    save_results_to_path(results=simulated_annealing_results, folder_path=SIMULATED_ANNEALING_PICKLES_PATH)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the main function with optional flags.")
    parser.add_argument("--example", type=int, help="Value for example flag (neighbors test).")
    parser.add_argument("--lower-complexity", type=int, help="Value for lower complexity flag.")
    parser.add_argument("--maximum-complexity", type=int, help="Value for maximum complexity flag.")
    args = parser.parse_args()

    example_flag = args.example if args.example else 0
    lower_complexity = args.lower_complexity if args.lower_complexity else 0
    maximum_complexity = args.maximum_complexity if args.maximum_complexity else 0

    main(lower_complexity=lower_complexity, maximum_complexity=maximum_complexity, example=example_flag)

