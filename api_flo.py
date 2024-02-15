from util.imports import * 
from util.objects import *
from util.helpers import *
from util.variables import *

app = FastAPI()

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
logger = logging.getLogger()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_storehouse():
    storehouse = parse_config('config.json')[2]
    return storehouse

def get_journeys(folder_path):
    results_dict = {}
    for file in os.listdir(folder_path):
        if file.endswith(".pickle"):
            chemin_file = os.path.join(folder_path, file)
            
            with open(chemin_file, "rb") as f:
                pickle_objects = pickle.load(f)
            pickle_objects
            filename = file.split('.')[0]
            if filename not in results_dict:
                results_dict[filename] = []

            for journey in pickle_objects:
                results_dict[filename].append(journey.to_dict()) 
                
    return results_dict

@app.get("/get_results")
def get_results():

    storehouse = get_storehouse()
    hill_climbing_results = get_journeys(folder_path=HILL_CLIMBING_RESULTS_PATH)
    simulated_annealing_results = get_journeys(folder_path=SIMULATED_ANNEALING_PATH)
    return  {
        "hill_climbing_results": hill_climbing_results,
        "simulated_annealing_results": simulated_annealing_results
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)