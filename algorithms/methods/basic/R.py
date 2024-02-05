from util.imports import * 
from util.objects import *
from util.helpers import *
from util.common import *

from algorithms.helpers import get_starting_time, get_available_tanks, get_valid_choices, check_storehouse_return

# Logs 
logging.basicConfig(level=logging.INFO)
file_handler = logging.FileHandler('logs/run_random.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Ajouter le gestionnaire de fichier au logger racine
logging.getLogger().addHandler(file_handler)
def run(tanks, parameters, storehouse, agent):    
    # Optimization 
    now = datetime.now() # + timedelta(days=1) : pour plus tard car on veut prédire le jour suivant
    starting_constraint = datetime(now.year, now.month, now.day)
    processing_journey = True
    journey = Journey()
    
    while(processing_journey):
        # Break if it exceeds the day
        if starting_constraint >= now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1):
            break

        starting_time = get_starting_time(tanks=tanks, agent=agent, starting_constraint=starting_constraint)
        # logging.info(f"Début journey")
        # colored(starting_time, "red", print=False)
        processing_cycle = True
        cycle = Cycle(starting_time=starting_time)
        
        while(processing_cycle):
            # logging.info(f'début while cycle : {cycle.total_volume}, tanks : {cycle.selected_tanks}')
            # Getting the available tanks (treatment of time window constraint)
            available_tanks = get_available_tanks(starting_time=starting_time+timedelta(minutes=cycle.total_time), cycle=cycle, tanks=tanks, storehouse=storehouse, parameters=parameters)
            
            if not available_tanks:
                # logging.info("Aucun tanks disponibles sur ce timing -> retour au dépôt et démarrage sur la prochaine plage")
                if not cycle.is_empty():
                    cycle.storehouse_return(parameters=parameters)
                    journey.add(cycle=cycle)
                    starting_constraint = cycle.starting_time + timedelta(minutes=cycle.total_time)
                else :
                    starting_constraint = cycle.starting_time + timedelta(minutes=60)
                # logging.info(f"Cycle starting time : {cycle.starting_time}, Starting constraint : {starting_constraint}")
                processing_cycle = False
                continue

            # Getting the valid tanks (treatment of quantity constraint)
            valid_tanks = get_valid_choices(tanks=available_tanks, cycle=cycle, parameters=parameters)
            
            if not valid_tanks:
                # logging.info("Aucun tanks ne peut être collecté -> plus assez de place dans la cuve retour au dépôt et lancement d'un nouveau cycle")
                cycle.storehouse_return(parameters=parameters)
                journey.add(cycle=cycle)
                starting_constraint = cycle.starting_time + timedelta(minutes=cycle.total_time)
                processing_cycle = False
                continue

            # Getting the final candidates (treatment of the agent working time constraint)
            final_candidates = check_storehouse_return(tanks=valid_tanks, cycle=cycle, storehouse=storehouse, parameters=parameters)

            if not final_candidates:
                # logging.info("Plus assez de temps de travail pour collecter par rapport à l'agent -> on retourne au dépôt et on cloture la journée de collecte")
                if not cycle.is_empty():
                    cycle.storehouse_return(parameters=parameters)
                    journey.add(cycle=cycle)
                    starting_constraint = cycle.starting_time + timedelta(minutes=cycle.total_time)
                processing_journey = False
                processing_cycle = False
                continue
            
            else : 
                # We choose a candidate (tank) to add to our cycle
                tank = random.choice(final_candidates)
                # We remove it from the candidates remaining
                tanks.remove(tank)
                # logging.info(f"update : tank id : {tank.id}, volume : {tank.current_volume}")
                # colored(cycle.total_time, "blue", "total_time before update", print=False)
                cycle.update(choice=tank, parameters=parameters)
                # colored(cycle.total_time, "blue", "total_time after update", print=False)
                # logging.info(f"before cycle total volume is {cycle.total_volume}")
                # logging.info(f"after cycle total volume is {cycle.total_volume}")
            # logging.info("fin while cycle")
    # logging.info("#-----------------------------------------------------------#")
    return journey 