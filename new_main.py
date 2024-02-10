from util.imports import *
from util.locations import *
from util.helpers import *
from util.objects import *
from util.datamodule import get_data

from algorithms.new_helpers import *
from algorithms.new_run import new_run

def main():
    # Récupération des données
    measurements, tanks, makers = get_data()

    # Récupération de la config
    constraints, vehicle, storehouse, agent = parse_config('new_config.json')

    # Filtrage par jours d'ouverture
    tanks = filter_days(tanks=tanks)
    
    # Filtrage par quantité 
    tanks = filter_quantities(tanks=tanks, constraints=constraints)

    # Génération des slots
    time_slots = generate_time_slots(tanks=tanks, constraints=constraints, agent=agent)

    # Génération des inputs de l'algo
    optimization_parameters_list = generate_optimization_paremeters(tanks=tanks, constraints=constraints, vehicle=vehicle, storehouse=storehouse, agent=agent, time_slots=time_slots)
    for optimization_parameters in optimization_parameters_list:
        new_run(optimization_parameters=optimization_parameters)
        break
        
# Appel de la fonction main
if __name__ == "__main__":
    main()
