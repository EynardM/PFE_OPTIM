from util.imports import *
from util.locations import *
from util.helpers import *
from util.objects import *
from util.datamodule import get_data

from algorithms.helpers import *
from algorithms.run import *
from optim.permutation import *


def main():
    # Récupération des données
    measurements, tanks, makers = get_data()

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
    visited_journeys = {}  
    optimization_parameters_list = generate_optimization_paremeters(tanks=tanks, constraints=constraints, vehicle=vehicle, storehouse=storehouse, agent=agent, time_slots=time_slots)
    for optimization_parameters in optimization_parameters_list:
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

        permutation(journey=journey, tanks=tanks, optimization_parameters=optimization_parameters)
        journeys.append(journey)
        score, volume, distance, emergency = journey.evaluation(tanks=tanks)
        solutions.append({"method": optimization_parameters.method, "score": score, "volume": volume, "distance": distance, "emergency": emergency})
        # print(json.dumps(journey.to_dict(), indent=4)) 
    print(len(journeys))
    # plot_pareto_front_3d(solutions)

# Appel de la fonction main
if __name__ == "__main__":
    main()

