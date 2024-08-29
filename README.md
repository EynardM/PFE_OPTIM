# <div align="center">Multi-Trip Vehicle Routing Problem with Time Windows </div>

## <div align="center">Research Paper</div>
Before diving into the project details, you may want to review the research paper that forms the basis of this project. It provides a comprehensive explanation of the methodology, use case, and results. You can find it at the root of this repository under the filename `research_paper.pdf`.

## <div align="center">First Install<div align="center">
Before doing anything else, make sure to install the required Python packages listed in `requirements.txt`. Run this:
```
pip install -r requirements.txt
```

## <div align="center">Data Overview</div>

The dataset comprises several CSV files, each providing essential information for managing the oil collection process:

1. **`collectors.csv`**: Contains details about the collectors responsible for moving the tank through the city. Each collector is assigned a unique identifier (`id`) and includes information such as their address, the company they work for, etc.

2. **`makers.csv`**: Holds comprehensive data about clients, encompassing their address, opening hours for oil collection, and details about the tanks on their premises, each identified by a unique ID.

3. **`tanks.csv`**: Contains crucial information regarding the oil tanks, including their unique IDs, capacity, and current fill level. This data is vital for the optimization algorithm.

4. **`measurements.csv`**: Provides data on measurements taken at various moments in different tanks. This information is likely instrumental for monitoring and analysis purposes.

5. **`fillings_stat.csv`**: Offers insights into the filling level habits of each client. This data proves valuable for assessing urgency and determining when to prioritize emptying a tank.

The collective information from these files forms a comprehensive dataset for efficiently managing the oil collection process, optimizing routes, and responding to client needs promptly.


## <div align="center">Algorithm</div>

First in **`helpers.py`** there are a lot of useful function:

- **generate_time_slots**: Generates time slots based on tank availability, agent constraints, and working hours.

- **generate_optimization_parameters**: Generates a list of optimization parameters for various methods and time slots.

- **get_starting_time**: Determines the starting time for a journey based on tank availability and agent constraints.

- **calculate_distance**: Calculates the distance between two geographical coordinates using the Haversine formula.

- **filter_hours**: Filters available tanks based on distance and time constraints.

- **filter_enough_filled**: Filters tanks based on their fill level and capacity.

- **filter_return**: Filters tanks based on return time constraints.

- **choice_function**: Selects a tank based on a specified method, which can be:
    - **R**: Random choice among available tanks.
    - **Q**: Quantity, choosing the fullest tank.
    - **D**: Distance, selecting the nearest tank by the algorithm.
    - **E**: Emergency, choosing the tank with the highest emergency level.
    - **HQD - HQE - HDE - HQDE:** These are heuristics combining the methods above.
    - **Random**: Chooses a random method among all the above ones to get the next tank.

Then we have the implementation of those different functions in the **`run.py`**, where the objective is to create an entire journey:
- **run_slot**: Creates a feasible cycle for one time slot within a journey. It utilizes various functions from **`helpers.py`** because the cycle needs to respect constraints.
- **run**: In this function, a complete journey is created by using `run_slot` several times, generating different cycles with a good combination.

## <div align="center">Optimization</div>

To improve our algorithm, we created journey neighbors, in **`neighbors.py`** with the **get_neighbors** function. We had three different way to create neighbors. 

### Permutation
The first method we employed is **permutation**. This method entails selecting a tank that was not initially included in the regular journey and replacing it with one of the currently scheduled tanks. From there the basic algorithm is running to recreate the end of the cycle. Except this cycle, the rest of the journey is unchanged. All functions related to this method can be found in **`permutation.py`**:

- **get_unused_tanks**: Obtains a list of tanks that haven't been used in the journey.

- **is_available**: Checks if a tank is available at a specific time within a cycle, filtering unused tanks based on hours.

- **get_available_cycles_positions**: Retrieves available positions within cycles where a tank can be inserted.

- **get_unchanged_cycle**: Retrieves a copy of the cycle up to the chosen position.

- **get_remaining_tanks**: Retrieves a list of tanks remaining after inserting a tank into a cycle.

- **update_choice_attributes**: Updates attributes of the chosen tank based on the current cycle.

- **check_choice**: Verifies if the chosen tank can be accommodated within the cycle based on time constraints.

- **filter_hours_cycle**: Filters tanks based on their availability within a cycle.

- **filter_enough_filled_cycle**: Filters tanks based on their filled capacity within a cycle.

- **filter_return_cycle**: Filters tanks based on their return time within a cycle.

- **optim_cycle**: Optimizes a cycle by inserting a tank at a specific position.

- **generate_neighbour_journey**: Generates a new journey by replacing a cycle with an optimized cycle.

- **permutation**: Generates new journeys by permuting tanks within cycles.
### Swap

The second method used in this optimization process is the **swap** method. This method involves verifying whether, within a cycle or even the entire journey, two tanks can be swapped to potentially improve the overall journey. The functions related to this method are implemented in the **`swap.py`** file.

- **get_arrival_time**: Obtains the arrival time of each tank in the journey.

- **available_swap**: Checks if a swap between two tanks is available based on their availability times.

- **get_possible_swaps**: Gets possible tank swaps based on their arrival times.

- **get_cycles_tanks**: Gets the tanks in each cycle after swapping a pair of tanks.

- **update_current_volume**: Updates the current volume of a tank based on a list of tanks.

- **update_attributes**: Updates attributes of a tank in a cycle.

- **update_return**: Updates the return time of a tank in a cycle.

- **try_reduce_collectable_volume**: Tries to reduce the collectable volume of a tank.

- **optim_swap**: Optimizes tank swap in a journey.

- **swap**: Swaps tanks in a journey.

### Transfer
The third method employed for generating neighboring solutions is the **transfer**. The principle is straightforward: within the journey, a tank is randomly removed from the selected tanks, and then the basic algorithm recalculates the rest of the journey. Every line of code related to this method can be found in **`transfer.py`**

- **get_selected_tanks_ids**: Obtain the IDs of tanks selected in a journey.
- **get_reduced_tanks**: Retrieve the list of tanks with one tank removed based on the tank ID.
- **transfer**: Transfer selected tanks to new journeys.

## <div align="center">Main</div>

In the **`main.py`**, we provide details about the different optimization algorithms used:

- **get_basic_journeys**: Generates basic journeys based on optimization parameters and tank data. It retrieves configuration parameters, filters tanks based on open days and quantity constraints, generates time slots for journeys, and then creates journeys with different combinations of tanks and time slots.

- **hill_climbing**: Performs the hill climbing optimization algorithm to find the best journey. It iteratively explores neighboring solutions, and if a better solution is found, it continues the search in that direction. This function can run with maximum or lower complexity based on the flag provided.

- **simulated_annealing**: Performs the simulated annealing optimization algorithm to find the best solution. It starts with an initial solution and iteratively explores neighboring solutions, accepting worse solutions with a certain probability. This probability decreases over time, allowing the algorithm to escape local optima. This function can run with maximum or lower complexity depending on the flag provided.

### Flags Used in main.py

- **Lower Complexity Flag** (`--lower-complexity`): This flag is used to specify the number of journeys for which the optimization algorithms will run with lower complexity. Lower complexity means that the optimization algorithms, hill climbing, and simulated annealing will not exhaustively explore all possible neighboring solutions but will instead stop after a certain number of iterations. This flag allows for quicker optimization runs when exhaustive search is not necessary.

- **Example Flag** (`--example`): This flag is used to specify the number of journeys for which an example demonstration will be performed. In this demonstration, the optimization algorithms will generate neighbors for the specified number of journeys using all available techniques (permutation, swap, transfer). This demonstration provides insight into how the optimization algorithms explore different solutions for a given journey.

- **Maximum Complexity Flag** (`--maximum-complexity`): This flag is included in case we want to generate all possible solutions with all the neighbor methods created. This means that if there are 100 permutations possible for a journey, the optimization will be run on all possibilities. Otherwise, it will choose one, get a new journey, and then optimize with both hill climbing and simulated annealing.

### Command Line Example:

You must choose at least one flag to initiate an optimization. However, you can include multiple flags in a single command to perform different types of optimizations simultaneously. For example:
```
python main.py --example 5 --lower-complexity 10 --maximum-complexity 20
```
This command will run the main function with the following configurations:
- Generate examples for 5 journeys.
- Run optimization algorithms with lower complexity for 10 journeys.
- Run optimization algorithms with maximum complexity for 20 journeys.
- 
## <div align="center">Config</div>


In the **`config.json`** file, you have the flexibility to customize configurations for various entities related to the optimization problem:

- **constraints**: Describes values for different constraints in the problem.
- **vehicle**: Defines attributes of the vehicle, including speed, capacity, and draining speed.
- **storehouse**: Specifies the location of the storehouse, where the agent unloads their cargo.
- **agent**: Provides details about the agent, including their name and working days and hours.

## <div align="center">Util</div>

In the **util** folder there are some interesting things.
### Objects
In **`object.py`**, there are all the classes that we have manipulated through this project: 
- **`Constraints`**: Represents constraints for the optimization problem, such as maximum working time, minimum draining volume, maximum simulation depth, and percentage volume threshold.

- **`Vehicle`**: Describes attributes of a vehicle, including its ID, name, capacity, speed, loading time, draining speed, and pumping speed.

- **`Storehouse`**: Represents a storehouse with properties like ID, latitude, longitude, and collector information.

- **`Agent`**: Represents an agent with details like ID, name, surname, working days, begin hour, and daily working slot.

- **`OptimizationParameters`**: Encapsulates parameters for optimization, including an agent, storehouse, date, tanks, constraints, vehicle, collector, and method.

- **`Measurement`**: Represents a measurement with various attributes such as ID, drainage, event type, fill level, filling, key maker, key tank, measured height, and volume.

- **`Tank`**: Describes a tank with properties like barcode, collector, overflow capacity, last reading date, tank type, nominal capacity, current volume, and fill level.

- **`Maker`**: Represents a maker with information like keys to tanks, collector, vacation details, address, hours, and geographical coordinates.

- **`Cycle`**: Represents a cycle in the optimization process, including starting and ending times, selected tanks, collected quantities, travel distances, and cycle statistics.
    
- **`Journey`**: Encapsulates a journey composed of cycles, including starting and ending times, journey time, journey volume, journey distance, and break time.



### Helper
In `helpers.py`, we've gathered various utility functions used for plotting, generating, obtaining, and saving results throughout the project:
- **parse_config**: Parse configuration from a JSON file and create instances of Constraints, Vehicle, Storehouse, and Agent.

- **create_maker_objects_from_dataframe**: Create a list of Maker objects from a DataFrame.

- **create_tank_objects_from_dataframe**: Create a list of Tank objects from a DataFrame.

- **create_measurement_objects_from_dataframe**: Create a list of Measurement objects from a DataFrame.

- **filter_days**: Filter tanks based on the working days of the associated makers.

- **filter_quantities**: Filter tanks based on the percentage volume threshold.

- **get_eval_weights**: Calculate evaluation weights based on the maximum volume, distance, and emergency in a list of journeys.

- **get_pareto_front**: Identify the Pareto front from a list of solutions.

- **plot_pareto_front**: Plot and save the Pareto front for a specific journey.

- **get_results**: Analyze and save results based on solutions, delta_days, and folder_path.

- **generate_progress_graph**: Generate and save a progress graph based on optimization progress.

- **save_results_to_path**: Save optimization results to pickle files in the specified folder.

- **save_solutions**: Save optimization solutions to an Excel file.

- **generate_box_plot**: Generate and save box plots from an Excel file.

- **get_journeys**: Reads pickle files from a specified folder, loads the pickled objects, and organizes them into a dictionary.

- **plot_comp_optim_methods**: Compares the optimization results of different methods by plotting their scores and generating a 3D scatter plot of the Pareto front.


### Reamaining files
- `datamodule.py` contains a function responsible for extracting data from a CSV file located in the data folder.

- The `variables.py` file defines constants, including choices for different methods used in the project.

- `locations.py` initializes file paths necessary for the project, providing a centralized place for managing file locations.

- `import.py` includes all the Python packages imported and utilized in this project.

- Within `decorator.py`, you'll find a function designed to calculate the execution time of another function. This can be useful for profiling and performance analysis.



## <div align="center">Results</div>

### Basic Folder

In the `basic` folder, you can find box plots and Pareto fronts for six different days, representing distinct journeys. Each day corresponds to a journey made during workday hours by an agent. The scores obtained by different choice methods are available in `values.xlsx`, and the percentage of the journey on the Pareto front following each choice method is provided in `percentages_on_pareto_front.xlsx`.

### Current_run Folder

The `current_run` folder contains similar information but only for the current journey.

### Optim Folder

#### Hill Climbing and Simulated Annealing
In the `optim` folder, graphs related to the optimization of journeys using either hill climbing or simulated annealing are available. Corresponding scores and metrics are stored in pickle files.

#### Neighbors Folder

Within the `neighbors` folder, you can find Pareto fronts and box plots based on different neighbor creation methods: Permutation, Swap, and Transfer. It is observed that the permutation method allows for a greater number of possible configurations, resulting in better outcomes compared to the other two methods.


## <div align="center">Front</div>

To enhance the interactivity of our solution, we have developed a web interface using `React` and `FastAPI`. This platform allows users to explore the various optimized steps of both the **`Hill Climbing`** and **`Simulated Annealing`** methods. Additionally, users can visualize the detailed planning for each optimized journey, providing a more interactive and informative experience.

To launch the app you first need to launch the API, that gets the data, by this command at the root of the repo:
```bash
python3 api.py
```
If you have never launched the app before, you need to install the required packages with the following command: 
```bash
npm --prefix front install
```
Once the installation is complete, you can launch the app with: 
```bash
npm --prefix front start
```

## <div align="center"> Here is a brief demo of the App on my computer</div>
<div align="center">
<img src="video/Demo_Web_App.gif" alt="Local GIF">
</div>



## <div align="center">Contributors</div>

### <div align="center">Florian BERGERE - Maxime EYNARD - Yann LANGLO - Amaury PETERSCHMITT</div>
