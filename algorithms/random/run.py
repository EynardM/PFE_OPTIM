from util.imports import * 
from util.objects import *
from algorithms.random.helpers import get_starting_time, get_available_tanks, get_valid_choices, check_storehouse_return

# Logs 
logging.basicConfig(level=logging.INFO)
file_handler = logging.FileHandler('logs/random.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Ajouter le gestionnaire de fichier au logger racine
logging.getLogger().addHandler(file_handler)
def run(tanks, parameters, storehouse, agent):    
    # Optimization 
    now = datetime.now()
    starting_constraint = datetime(now.year, now.month, now.day)
    processing_journey = True
    journey = Journey()
    
    while(processing_journey):
        logging.info('début journey')
        starting_time = get_starting_time(tanks=tanks, agent=agent, starting_constraint=starting_constraint)

        processing_cycle = True
        cycle = Cycle(starting_time=starting_time)
        
        while(processing_cycle):
            logging.info('début while cycle')
            # Getting the available tanks (treatment of time window constraint)
            available_tanks = get_available_tanks(starting_time=starting_time+timedelta(minutes=cycle.total_time), cycle=cycle, tanks=tanks, storehouse=storehouse, parameters=parameters)
            
            if not available_tanks:
                logging.info("Aucun tanks disponibles sur ce timing -> retour au dépôt et démarrage sur la prochaine plage")
                cycle.storehouse_return(parameters=parameters)
                journey.add(cycle=cycle)
                starting_constraint = cycle.starting_time + timedelta(minutes=cycle.total_time)
                processing_cycle = False
                

            # Getting the valid tanks (treatment of quantity constraint)
            valid_tanks = get_valid_choices(tanks=available_tanks, cycle=cycle, parameters=parameters)
            
            if not valid_tanks:
                logging.info("Aucun tanks ne peut être collecté -> plus assez de place dans la cuve retour au dépôt et lancement d'un nouveau cycle")
                cycle.storehouse_return(parameters=parameters)
                journey.add(cycle=cycle)
                starting_constraint = cycle.starting_time + timedelta(minutes=cycle.total_time)
                processing_cycle = False

            # Getting the final candidates (treatment of the agent working time constraint)
            final_candidates = check_storehouse_return(tanks=valid_tanks, cycle=cycle, storehouse=storehouse, parameters=parameters)
            if not final_candidates:
                logging.info("Plus assez de temps de travail pour collecter par rapport à l'agent -> on retourne au dépôt et on cloture la journée de collecte")
                cycle.storehouse_return(parameters=parameters)
                journey.add(cycle=cycle)
                processing_journey = False
                processing_cycle = False
            
            else : 
                # We choose a candidate (tank) to add to our cycle
                tank = random.choice(final_candidates)
                cycle.update(choice=tank, parameters=parameters)
            logging.info("fin while cycle")
    return journey 