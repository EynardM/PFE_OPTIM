# Multi-Trip Vehicle Routing Problem with Time Windows 

## Data Overview

The dataset comprises several CSV files, each providing essential information for managing the oil collection process:

1. **`collectors.csv`**: Contains details about the collectors responsible for moving the tank through the city. Each collector is assigned a unique identifier (`id`) and includes information such as their address, the company they work for, etc.

2. **`makers.csv`**: Holds comprehensive data about clients, encompassing their address, opening hours for oil collection, and details about the tanks on their premises, each identified by a unique ID.

3. **`tanks.csv`**: Contains crucial information regarding the oil tanks, including their unique IDs, capacity, and current fill level. This data is vital for the optimization algorithm.

4. **`measurements.csv`**: Provides data on measurements taken at various moments in different tanks. This information is likely instrumental for monitoring and analysis purposes.

5. **`fillings_stat.csv`**: Offers insights into the filling level habits of each client. This data proves valuable for assessing urgency and determining when to prioritize emptying a tank.

The collective information from these files forms a comprehensive dataset for efficiently managing the oil collection process, optimizing routes, and responding to client needs promptly.


## Algorithm

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

## Optimization

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
## Swap

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

## Main

In the **`main.py`**, we provide details about the different optimization algorithms used:

- **get_basic_journeys**: Generates basic journeys based on optimization parameters and tank data. It retrieves configuration parameters, filters tanks based on open days and quantity constraints, generates time slots for journeys, and then creates journeys with different combinations of tanks and time slots.

- **hill_climbing**: Performs the hill climbing optimization algorithm to find the best journey. It iteratively explores neighboring solutions, and if a better solution is found, it continues the search in that direction. This function can run with maximum or lower complexity based on the flag provided.

- **simulated_annealing**: Performs the simulated annealing optimization algorithm to find the best solution. It starts with an initial solution and iteratively explores neighboring solutions, accepting worse solutions with a certain probability. This probability decreases over time, allowing the algorithm to escape local optima. This function can run with maximum or lower complexity depending on the flag provided.

### What is the maximum complexity flag?

The maximum complexity flag is included in case we want to generate all possible solutions with all the neighbor methods created. This means that if there are 100 permutations possible for a journey, the optimization will be run on all possibilities. Otherwise, it will choose one, get a new journey, and then optimize with both hill climbing and simulated annealing.

- **main**: The main function executes optimization algorithms. It initializes data, runs the `get_basic_journeys` function, and optionally runs examples, hill climbing with maximum complexity, and simulated annealing with both maximum and lower complexity based on the flags provided.

## Config

## Config

In the **`config.json`** file, you have the flexibility to customize configurations for various entities related to the optimization problem:

- **constraints**: Describes values for different constraints in the problem.
- **vehicle**: Defines attributes of the vehicle, including speed, capacity, and draining speed.
- **storehouse**: Specifies the location of the storehouse, where the agent unloads their cargo.
- **agent**: Provides details about the agent, including their name and working days and hours.


## Result
## Front