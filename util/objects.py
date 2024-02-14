from util.imports import * 
from util.common import *
from util.variables import *

class Constraints:
    def __init__(self, max_working_time, min_draining_volume, max_simulation_deepness, percentage_volume_threshold):
        self.max_working_time = max_working_time
        self.min_draining_volume = min_draining_volume
        self.max_simulation_deepness = max_simulation_deepness
        self.percentage_volume_threshold = percentage_volume_threshold

    def __str__(self):
        return f"Constraints(max_working_time={self.max_working_time}, min_draining_volume={self.min_draining_volume}, " \
               f"max_simulation_deepness={self.max_simulation_deepness}, " \
               f"percentage_volume_threshold={self.percentage_volume_threshold})"


    def to_dict(self):
        return {
            "max_working_time": self.max_working_time,
            "min_draining_volume": self.min_draining_volume,
            "max_simulation_deepness": self.max_simulation_deepness,
            "percentage_volume_threshold": self.percentage_volume_threshold
        }
    
class Vehicle:
    def __init__(self, id: str, name: str, capacity: float, speed: float, loading_time: float, \
            draining_speed: float, pumping_speed: float) -> None:
        self.id = id
        self.name = name
        self.capacity = capacity
        self.speed = speed
        self.loading_time = loading_time
        self.draining_speed = draining_speed
        self.pumping_speed = pumping_speed


    def __str__(self):
        return f"Vehicle(id={self.id}, name={self.name}, capacity={self.capacity}, speed={self.speed}, " \
               f"loading_time={self.loading_time}, draining_speed={self.draining_speed}, " \
               f"pumping_speed={self.pumping_speed})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
            "speed": self.speed,
            "loading_time": self.loading_time,
            "draining_speed": self.draining_speed,
            "pumping_speed": self.pumping_speed
        }
    
class Storehouse:
    def __init__(self, id: str, latitude: float, longitude: float, collector: str):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.collector = collector

    def __str__(self):
        return f"Storehouse(id={self.id}, latitude={self.latitude}, longitude={self.longitude}, " \
               f"collector={self.collector})"

    def get_coordinates(self, rad=True):
        if rad: 
            return radians(self.latitude), radians(self.longitude)
        else: 
            return self.latitude, self.longitude
    
    def to_dict(self):
        return {
            "id": self.id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "collector": self.collector
        }
    
class Agent:
    def __init__(self, id: str, name: str, surname: str, working_days: List[int], begin_hour: int, daily_working_slot=None):
        self.id = id
        self.name = name
        self.surname = surname
        self.working_days = working_days
        self.begin_hour = datetime.combine(datetime.now().date(), datetime.min.time()) + timedelta(hours=begin_hour)
        self.daily_working_slot = daily_working_slot

    def nb_of_slots(self):
        return sum(2 if isinstance(slot, tuple) else 1 for slot in self.daily_working_slot)//2
    
    def __str__(self):
        return f"Agent(id={self.id}, name={self.name}, surname={self.surname}, " \
               f"working_days={self.working_days}, begin_hour={self.begin_hour}, " \
               f"daily_working_slot={self.daily_working_slot})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "working_days": self.working_days,
            "begin_hour": self.begin_hour.strftime("%Y-%m-%d %H:%M:%S") if self.begin_hour else None,
            "daily_working_slot": self.daily_working_slot
        }    
    
class OptimizationParameters:
    def __init__(self, agent, storehouse, date, tanks, constraints, vehicle, collector=None, method=None):
        self.agent = agent
        self.vehicle = vehicle
        self.storehouse = storehouse
        self.date = date
        self.tanks = tanks
        self.constraints = constraints
        self.collector = collector
        self.method = method

    def __str__(self):
        colored(self.agent, "green", "agent")
        colored(self.vehicle, "green", "vehicule")
        colored(self.storehouse, "green", "storehouse")
        colored(self.date, "green", "date")
        colored(self.constraints, "green", "constraints")
        colored(self.method, "green", "method")
        return ""

class Measurement:
    def __init__(self, id, drainage, event_type_id, event_type_label, fill_level,
                 filling, key_maker, key_tank, measured_height, measurement_date,
                 measurement_status_id, measurement_status_label, note_type_id,
                 note_type_label, vidange, volume):
        self.id = id
        self.drainage = drainage
        self.event_type_id = event_type_id
        self.event_type_label = event_type_label
        self.fill_level = fill_level
        self.filling = filling
        self.key_maker = key_maker
        self.key_tank = key_tank
        self.measured_height = measured_height
        self.measurement_date = measurement_date
        self.measurement_status_id = measurement_status_id
        self.measurement_status_label = measurement_status_label
        self.note_type_id = note_type_id
        self.note_type_label = note_type_label
        self.vidange = vidange
        self.volume = volume

    def __str__(self):
        return (f"Measurement ID: {self.id}\n"
                f"Drainage: {self.drainage}\n"
                f"Event Type ID: {self.event_type_id}\n"
                f"Event Type Label: {self.event_type_label}\n"
                f"Fill Level: {self.fill_level}\n"
                f"Filling: {self.filling}\n"
                f"Key Maker: {self.key_maker}\n"
                f"Key Tank: {self.key_tank}\n"
                f"Measured Height: {self.measured_height}\n"
                f"Measurement Date: {self.measurement_date}\n"
                f"Measurement Status ID: {self.measurement_status_id}\n"
                f"Measurement Status Label: {self.measurement_status_label}\n"
                f"Note Type ID: {self.note_type_id}\n"
                f"Note Type Label: {self.note_type_label}\n"
                f"Vidange: {self.vidange}\n"
                f"Volume: {self.volume}\n")
     
class Tank:
    def __init__(self, barcode, collector, overflow_capacity, last_reading_date, tank_type_label,
                 tank_type_id, nominal_capacity, container_type_label, tank_name, key_maker,
                 container_type_id, tank_status_label, current_volume, tank_id, tank_status_id,
                 fill_level):
        self.barcode = barcode
        self.collector = collector
        self.overflow_capacity = overflow_capacity
        self.last_reading_date = last_reading_date
        self.tank_type_label = tank_type_label
        self.tank_type_id = tank_type_id
        self.nominal_capacity = nominal_capacity
        self.container_type_label = container_type_label
        self.tank_name = tank_name
        self.key_maker = key_maker
        self.container_type_id = container_type_id
        self.tank_status_label = tank_status_label
        self.current_volume = current_volume
        self.id = tank_id
        self.tank_status_id = tank_status_id
        self.fill_level = fill_level
        self.maker = None
        self.mean_nonzeros_fill = None
        self.std_nonzeros_fill = None
        self.mean_zeros_fill_seq = None
        self.std_zeros_fill_seq = None
        self.filling_vector = None
        self.distance = None
        self.time_to_go = None
        self.collectable_volume = None
        self.manoever_time = None
        self.time_to_storehouse = None
        self.return_time = None

    def __str__(self):
        return f"Tank ID: {self.id}, Name: {self.tank_name}, Barcode: {self.barcode}, " \
               f"Collector: {self.collector}, Status: {self.tank_status_label}, " \
               f"Current Volume: {self.current_volume}, Fill Level: {self.fill_level}"
    
    def get_coordinates(self, rad=True):
        if rad: 
            return radians(self.maker.latitude), radians(self.maker.longitude)
        else: 
            return self.maker.latitude, self.maker.longitude
    
    def is_available(self, dt: datetime):
        for start, end in self.maker.hours:
            if start <= dt <= end:
                return True
        return False
    
    def to_dict(self):
        maker_data = {
            "latitude": self.maker.latitude if self.maker else None,
            "longitude": self.maker.longitude if self.maker else None,
            "maker_name": self.maker.name if self.maker else None,
            "hours": self.maker.hours if self.maker else None,
            "days": self.maker.days if self.maker else None
        }

        return {
            "id": self.id,
            "current_volume": self.current_volume,
            "overflow_capacity": self.overflow_capacity,
            "maker": maker_data
        }
    
class Maker:
    def __init__(self, keys_tanks, collector, ending_vacation, days, opening_vacation,
                 address, hours, country, name, post_code, city, internal_name,
                 longitude, id, latitude):
        self.id = id
        self.longitude = longitude
        self.latitude = latitude
        self.keys_tanks = keys_tanks
        self.collector = collector
        self.ending_vacation = ending_vacation
        self.days = ast.literal_eval(days)
        self.opening_vacation = opening_vacation
        self.address = address
        self.hours = []
        for hour_range_str in ast.literal_eval(hours):
            hour_range_datetime = []
            for hour in hour_range_str:
                if hour == "24:00":
                    hour = "00:00"
                combined_datetime_str = f"{datetime.now().date()} {hour}"
                hour_range_datetime.append(datetime.strptime(combined_datetime_str, '%Y-%m-%d %H:%M'))
            self.hours.append(hour_range_datetime)
        self.country = country
        self.name = name
        self.post_code = post_code
        self.city = city
        self.internal_name = internal_name

    def __str__(self):
        return f"Maker(keys_tanks={self.keys_tanks}, collector={self.collector}, " \
               f"ending_vacation={self.ending_vacation}, days={self.days}, " \
               f"opening_vacation={self.opening_vacation}, address={self.address}, " \
               f"hours={self.hours}, country={self.country}, name={self.name}, " \
               f"post_code={self.post_code}, city={self.city}, " \
               f"internal_name={self.internal_name}, longitude={self.longitude}, " \
               f"id={self.id}, latitude={self.latitude})"

class Cycle:
    def __init__(self, starting_time, ending_time=None):
        self.starting_time = starting_time
        self.current_time = starting_time
        self.ending_time = ending_time
        self.potential_ending_time = None

        self.selected_tanks = []
        self.collected_quantities = []
        self.travel_distances = []
        self.travel_times = []
        self.manoever_times = []

        self.cycle_time = 0
        self.cycle_volume = 0
        self.cycle_distance = 0

    def __str__(self):
        tanks_ids = ", ".join([f"Tank : {tank.id}" for tank in self.selected_tanks])
        tanks_collected_quantities = ", ".join([f"Collected quantity : {quantity}" for quantity in self.collected_quantities])
        colored(self.starting_time, "green", "starting_time")
        colored(self.current_time, "green", "current_time")
        colored(self.ending_time, "green", "ending_time")
        colored(self.cycle_time, "blue", "cycle_time")
        colored(self.cycle_volume, "blue", "cycle_volume")
        colored(tanks_ids, "red")
        colored(tanks_collected_quantities, "red")
        return ""
    
    def add_tank(self, choice: Tank, optimization_parameters: OptimizationParameters):
        # Adding the tank
        self.selected_tanks.append(choice)

        # Updating quantities
        self.cycle_volume += choice.collectable_volume
        self.collected_quantities.append(choice.collectable_volume)
        choice.current_volume -= choice.collectable_volume

        # Updating distances
        self.travel_distances.append(choice.distance)
        self.cycle_distance = sum(self.travel_distances)

        # Updating times
        self.travel_times.append(choice.time_to_go)
        self.manoever_times.append(choice.manoever_time)
        self.cycle_time += choice.time_to_go + choice.manoever_time +  optimization_parameters.vehicle.loading_time

        self.current_time = self.starting_time + timedelta(minutes=self.cycle_time)
        self.potential_ending_time = self.current_time + timedelta(minutes=choice.return_time)

    def is_empty(self):
        return self.selected_tanks == []
    
    def get_last_point(self, storehouse: Storehouse):
        if self.is_empty():
            return storehouse
        else : 
            return self.selected_tanks[-1]

    def is_enough(self, constraints):
        return self.cycle_volume >= constraints.minimum_draining_volume
    
    def storehouse_return(self, optimization_parameters: OptimizationParameters):
        # Getting the last point
        last_tank = self.selected_tanks[-1]

        # Updating the travel times with the travel time to go from last point to storehouse
        self.travel_times.append(last_tank.time_to_storehouse)
        self.manoever_times.append(self.cycle_volume/optimization_parameters.vehicle.draining_speed)

        # Updating cycle values
        self.cycle_time += last_tank.return_time
        self.cycle_distance = sum(self.travel_distances)
        
        # Updating the ending time of the cycle
        self.ending_time = self.starting_time + timedelta(minutes=self.cycle_time)

    def to_dict(self):
        if self.ending_time is None:
            ending_time = None
        else :
            ending_time = self.ending_time.strftime("%Y-%m-%d %H:%M:%S")
        return {
            "starting_time": self.starting_time.strftime("%Y-%m-%d %H:%M:%S"),
            "current_time": self.current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "ending_time": ending_time,
            "selected_tanks": [tank.id for tank in self.selected_tanks],
            "collected_quantities": [quantity for quantity in self.collected_quantities],
            "cycle_time": self.cycle_time,
            "cycle_volume": self.cycle_volume,
            "cycle_distance": self.cycle_distance
        }
    
class Journey:
    def __init__(self, starting_time: datetime, ending_time: datetime, break_time=0):
        self.starting_time = starting_time
        self.current_time = starting_time
        self.ending_time = ending_time
        self.cycles = []

        self.break_time = break_time
        self.journey_time = 0
        self.journey_volume = 0
        self.journey_distance = 0
        self.journey_global_emergency = None

    def __str__(self):
        cycle_details = "\n".join([str(cycle) for cycle in self.cycles])

        return f"Start Time: {self.starting_time}, End Time: {self.ending_time}, Journey Time: {self.journey_time}, Journey Volume: {self.journey_volume}, Journey Distance: {self.journey_distance}, Break Time: {self.break_time}\nCycles:\n{cycle_details}"
    
    def __eq__(self, other):
        if not isinstance(other, Journey):
            return False
        
        return (self.starting_time == other.starting_time and
                self.ending_time == other.ending_time and
                self.journey_time == other.journey_time and
                self.journey_volume == other.journey_volume and
                self.journey_distance == other.journey_distance)

    def __hash__(self):
        return hash((self.starting_time, self.ending_time, self.journey_time, self.journey_volume, self.journey_distance))

    def add_cycle(self, cycle: Cycle) -> List[Cycle]:
        self.journey_time += cycle.cycle_time
        if not cycle.is_empty():
            self.cycles.append(cycle)
            self.journey_volume += cycle.cycle_volume
            self.journey_distance += cycle.cycle_distance

    def evaluation(self, tanks: List[Tank]):
        global weight_Q, weight_D, weight_E
        tanks_copy = deepcopy(tanks)
        for cycle in self.cycles:
            for i,tank_cycle in enumerate(cycle.selected_tanks):
                for tank in tanks_copy:
                    if tank_cycle.id == tank.id:
                        tank.current_volume -= cycle.collected_quantities[i]
        self.journey_global_emergency = np.mean([tank.current_volume / tank.overflow_capacity for tank in tanks_copy]) # add mean or max filling of each tank in the ratio 
        score = weight_Q * self.journey_volume + weight_D * self.journey_distance + weight_E * self.journey_global_emergency
        return score
    
    def to_dict(self):
        return {
            "start_time": self.starting_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": self.ending_time.strftime("%Y-%m-%d %H:%M:%S"),
            "cycles": [cycle.to_dict() for cycle in self.cycles],
            "journey_time": self.journey_time,
            "journey_volume": self.journey_volume,
            "journey_distance": self.journey_distance,
            "break_time": self.break_time
        }