from util.imports import *
from util.locations import *
from util.helpers import *
from util.objects import *

def get_selected_tank_coordinates(journey: Journey):
    cycles_coordinates = []
    for cycle in journey.cycles:
        cycle_coordinates = []
        for tank in cycle.selected_tanks:
            cycle_coordinates.append((tank.get_coordinates(rad=False)))
        cycles_coordinates.append(cycle_coordinates)
    return cycles_coordinates

# Chemin du dossier contenant les fichiers .pickle
dossier = HILL_CLIMBING_RESULTS_PATH

# Parcours du dossier
for fichier in os.listdir(dossier):
    if fichier.endswith(".pickle"):
        chemin_fichier = os.path.join(dossier, fichier)
        
        with open(chemin_fichier, "rb") as f:
            objet_pickle = pickle.load(f)
        
        print("Nom de fichier:", fichier)
        # Faire quelque chose avec l'objet pickle, par exemple :
        print("Contenu du fichier pickle:", objet_pickle)
        for journey in objet_pickle:
            print(journey.to_dict())
            break 
