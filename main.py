from util.imports import *
from util.locations import *
from util.helpers import *
from util.objects import *
from util.datamodule import get_data

from algorithms.methods.basic import R, D, E, Q
from algorithms.methods.heuristical import HQD, HQDE

methods = {
    "Random-choice": R,
    "Quantity-choice": Q,
    "Distance-choice": D,
    "Emergency-choice": E,
    "(H) Quantity-Distance-choice": HQD,
    "(H) Quantity-Distance-Emergency-choice": HQDE
}

def main():
    # Récupération des données
    measurements, tanks, makers = get_data()
    print(f"Nombre de cuves totales : {len(tanks)}")

    # Récupération des paramètres
    parameters, storehouse, agent = parse_config('config.json')

    # Filtrage par jours d'ouverture
    tanks = filter_days(tanks=tanks)
    print(f"Nombre de cuves post filtre jours : {len(tanks)}")
    
    # Filtrage par quantité 
    tanks = filter_quantities(tanks=tanks, parameters=parameters)
    print(f"Nombre de cuves post filtre quantités : {len(tanks)}")

    # Initialisation des données pour chaque algorithme
    algorithm_data = {}
    for name, method in methods.items():
        tanks_copy = [deepcopy(tank) for tank in tanks]
        journey = method.run(tanks=tanks_copy, parameters=parameters, storehouse=storehouse, agent=agent)
        journey.update(tanks=tanks_copy)  # Mettre à jour les données du voyage
        evaluation = journey.evaluation()
        # Assurez-vous que evaluation est un tuple (total_volume, total_distance, maximum_emergency, global_emergency)
        evaluation_tuple = (journey.total_volume, journey.total_distance, journey.global_emergency)
        algorithm_data[name] = {"journey": journey, "evaluation": evaluation_tuple}

    print(algorithm_data)
    plot_pareto_front_3d(algorithm_data=algorithm_data)
    return algorithm_data

if __name__ == "__main__":
    main()
