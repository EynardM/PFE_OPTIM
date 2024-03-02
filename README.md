# Vehicle Routing Optimization with Time Windows (PFE)

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


## Results/Main
## Front