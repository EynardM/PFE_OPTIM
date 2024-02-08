from util.imports import *
from util.locations import *
from util.helpers import *
from util.objects import *
from util.datamodule import get_data

from algorithms.helpers import *
from algorithms.run import run

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

    # Obtention des time slots possibles sans et avec pause
    time_slots_without_break, time_slots_with_break = generate_time_slots(tanks=tanks, parameters=parameters, agent=agent)
    time_slots = time_slots_without_break + time_slots_with_break

    # Call the algorithm for each combation of time slots
    journeys = []
    method_scores = {}

    for method in ["R", "Q", "D", "E", "HQD", "HQDE"]:
        for time_slot in time_slots:
            tanks_copy = [deepcopy(tank) for tank in tanks]
            
            nb_slots = int(count_total_elements(time_slot)/2)
            if nb_slots != 1: 
                time_slot_journeys = []
                for i in range(nb_slots):
                    start, end = time_slot[i]
                    journey = run(start=start, end=end, tanks=tanks_copy, parameters=parameters, storehouse=storehouse, agent=agent, method=method)
                    time_slot_journeys.append(journey)
                journey = concatenate_journeys(time_slot_journeys)
            else :
                start, end = time_slot
                journey = run(start=start, end=end, tanks=tanks_copy, parameters=parameters, storehouse=storehouse, agent=agent, method=method)

            if verify_journey(journey=journey, tanks=tanks, parameters=parameters, storehouse=storehouse):
                print(f"Compliance verified")
            else:
                print("Not compliant ")

            journeys.append(journey)
            score, volume, distance, emergency = journey.evaluation(tanks=tanks_copy)
            if method not in method_scores:
                method_scores[method] = []
            method_scores[method].append({"score": score, "volume": volume, "distance": distance, "emergency": emergency})
            print(json.dumps(journey.to_dict(), indent=4)) 
    
    plot_pareto_front_3d(method_scores)

if __name__ == "__main__":
    main()
