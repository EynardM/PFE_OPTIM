from util.imports import *  # Import necessary modules
from util.objects import *
from util.helpers import *
from util.variables import *
from util.datamodule import *

app = FastAPI()  # Create a FastAPI instance

# Configure logging
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
logger = logging.getLogger()

# Add CORS middleware to handle Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the coordinates of the storehouse from the config file
def get_storehouse():
    storehouse = parse_config('config.json')[2]
    return storehouse

# Function to retrieve journey data from pickle files in a given folder
def get_journeys(folder_path):
    measurements, tanks, makers = get_data()
    results_dict = {}

    # Iterate through pickle files in the specified folder
    for file in os.listdir(folder_path):
        if file.endswith(".pickle"):
            chemin_file = os.path.join(folder_path, file)
            
            with open(chemin_file, "rb") as f:
                pickle_objects = pickle.load(f)
            filename = file.split('.')[0]

            # Create a list for the specific filename if not exists
            if filename not in results_dict:
                results_dict[filename] = []

            # Calculate and add journey_score to each journey
            for journey in pickle_objects:
                score = journey.evaluation(tanks=tanks)
                new_journey = journey.to_dict()
                new_journey["journey_score"] = score
                results_dict[filename].append(new_journey) 
                
    return results_dict

# FastAPI route to get results
@app.get("/get_results")
def get_results():
    storehouse = get_storehouse()  # Get storehouse coordinates
    # Retrieve journey results for hill climbing and simulated annealing
    hill_climbing_results = get_journeys(folder_path=HILL_CLIMBING_PICKLES_LOWER_COMPLEXITY_PATH)
    simulated_annealing_results = get_journeys(folder_path=SIMULATED_ANNEALING_PICKLES_PATH)

    return  {
        "hill_climbing_results": hill_climbing_results,
        "simulated_annealing_results": simulated_annealing_results,
        "storehouse" : storehouse  # Return storehouse coordinates
    }

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
