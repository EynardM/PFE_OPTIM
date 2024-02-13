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
    parameters = []
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

        journeys.append(journey)
        for cycle in journey.cycles:
            current_time = cycle.starting_time
            for i,tank in enumerate(cycle.selected_tanks):
                arriving_time = current_time + timedelta(minutes=cycle.travel_times[i])
                colored(arriving_time, "red")
                current_time += timedelta(minutes=cycle.travel_times[i]+cycle.manoever_times[i]+optimization_parameters.vehicle.loading_time)
                colored(tank.maker.hours, "blue", "hours")

        break
"""        score, volume, distance, emergency = journey.evaluation(tanks=tanks)
        solutions.append({"method": optimization_parameters.method, "score": score, "volume": volume, "distance": distance, "emergency": emergency})
  
        new_journeys = permutation(journey=journey, tanks=tanks, optimization_parameters=optimization_parameters)
        unique_new_journeys = set(new_journeys)
        print(f"Unique journeys : {len(unique_new_journeys)}/{len(new_journeys)}")

        for new_journey in unique_new_journeys:
            score, volume, distance, emergency = new_journey.evaluation(tanks=tanks)
            solutions.append({"method": "Permutation", "score": score, "volume": volume, "distance": distance, "emergency": emergency})
  

    plot_pareto_front_3d(solutions)
    """

# Appel de la fonction main
if __name__ == "__main__":
    main()

