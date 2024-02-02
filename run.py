from util.imports import * 
from util.objects import *
from util.locations import *
from util.helpers import *
from util.datamodule import get_data
from run_helpers import filter_days, filter_quantities, get_start_hour

def run():
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
    
    # Optimization 
    start_hour = get_start_hour(tanks=tanks, agent=agent)
    print(f"Premier créneau horaire : {start_hour}")

    # Iterate over tanks available + Implement the ruless

if __name__ == "__main__":
    run()