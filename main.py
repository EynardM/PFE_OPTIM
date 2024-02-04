from util.imports import *
from util.locations import *
from util.helpers import *
from util.datamodule import get_data
from algorithms.random.run import run as algo_random_run

def main():
# Getting the data
    measurements, tanks, makers = get_data()
    print(f"Nombre de cuves totales : {len(tanks)}")

    # Getting parameters
    parameters, storehouse, agent = parse_config('config.json')
    
    # Filter by opening days
    tanks = filter_days(tanks=tanks)
    print(f"Nombre de cuves post filtre jours : {len(tanks)}")
    
    # Filter by quantity 
    tanks = filter_quantities(tanks=tanks, parameters=parameters)
    print(f"Nombre de cuves post filtre quantités : {len(tanks)}")

    #-----------------------------------------------------------#
    #----------LAUNCHING ALGORITHMS IN PARALLEL BELLOW----------#
    #-----------------------------------------------------------#
    algo_random_tanks = [deepcopy(tank) for tank in tanks]
    journey = algo_random_run(tanks=algo_random_tanks, parameters=parameters, storehouse=storehouse, agent=agent)
    for cycle in journey.cycles:
        print(cycle)
    
if __name__ == "__main__":
    main()