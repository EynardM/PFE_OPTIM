from util.imports import *
from util.locations import *
from util.helpers import *
from util.objects import *
from util.decorator import *
from util.datamodule import get_data

from algorithms.helpers import *
from algorithms.run import *
from optim.permutation import *
from optim.swap import *
from optim.transfer import *

@timeit
def get_basic_journeys(tanks: List[Tank]):
    # Récupération de la config
    constraints, vehicle, storehouse, agent = parse_config('config.json')

    # Filtrage par jours d'ouverture
    tanks = filter_days(tanks=tanks)
    
    # Filtrage par quantité 
    tanks = filter_quantities(tanks=tanks, constraints=constraints)

    # Génération des slots
    time_slots = generate_time_slots(tanks=tanks, constraints=constraints, agent=agent)

    # Génération des inputs de l'algo
    journeys = []
    solutions = []
    parameters = []
    visited_journeys = {}  
    optimization_parameters_list = generate_optimization_paremeters(tanks=tanks, constraints=constraints, vehicle=vehicle, storehouse=storehouse, agent=agent, time_slots=time_slots)
    for iter,optimization_parameters in enumerate(optimization_parameters_list):
        journey = run(optimization_parameters=optimization_parameters)
        
        # Vérifier si le `journey` est déjà présent pour cette méthode
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

        journeys.append(journey)
        parameters.append(optimization_parameters)
        score = journey.evaluation(tanks=tanks)
        solutions.append({"method": optimization_parameters.method, "score": score, "volume": journey.journey_volume, "distance": journey.journey_distance, "emergency": journey.journey_global_emergency})
  
    plot_pareto_front_3d(solutions, filename="basic_journeys.png")
    return solutions, journeys, parameters

@timeit
def hill_climbing(journey: Journey, tanks: List[Tank], optimization_parameters: OptimizationParameters) -> List[Journey]:
    best_journeys = [journey]

    iter = 0
    progress = True
    while(progress):
        print(f'iter : n°{iter}')
        best_journey = best_journeys[-1]
        permutation_journeys = permutation(journey=best_journey, tanks=tanks, optimization_parameters=optimization_parameters)
        swap_journeys = swap(journey=best_journey, tanks=tanks, optimization_parameters=optimization_parameters)
        transfer_journeys = transfer(journey=best_journey, tanks=tanks, optimization_parameters=optimization_parameters)
    
        new_journeys = []
        if permutation_journeys is not None:
            new_journeys += permutation_journeys
        if swap_journeys is not None:
            new_journeys += swap_journeys
        if transfer_journeys is not None:
            new_journeys += transfer_journeys

        progress = False
        for new_journey in new_journeys:
            if new_journey.evaluation(tanks=tanks) >= best_journey.evaluation(tanks=tanks):
                print('progress')
                progress = True
                best_journey = new_journey 
                best_journeys.append(best_journey)

        iter += 1 
    return best_journeys

@timeit
def main():
    # Récupération des données
    measurements, tanks, makers = get_data()

    solutions, journeys, parameters = get_basic_journeys(tanks=tanks)

    for i in range (len(journeys)):
        print(f'Journey n°{i}/{len(journeys)}')
        journey = journeys[i]
        parameter = parameters[i]
        best_journeys = hill_climbing(journey=journey, tanks=tanks, optimization_parameters=parameter)
        
# Appel de la fonction main
if __name__ == "__main__":
    main()

