from util.imports import * 

class Parameters:
    def __init__(self, simulation_deep: int, working_time: int, mobile_tank_volume: int,
                 vehicle_speed: int, loading_time: int, pumping_speed: int,
                 draining_speed: int, percentage_volume_threshold: float,
                 percentage_partial_collect_volume: float, minimum_draining_volume: int,
                 average_cycle_time: int):
        self.simulation_deep = simulation_deep
        self.working_time = working_time
        self.mobile_tank_volume = mobile_tank_volume
        self.vehicle_speed = vehicle_speed
        self.loading_time = loading_time
        self.pumping_speed = pumping_speed
        self.draining_speed = draining_speed
        self.percentage_volume_threshold = percentage_volume_threshold
        self.percentage_partial_collect_volume = percentage_partial_collect_volume
        self.minimum_draining_volume = minimum_draining_volume
        self.average_cycle_time = average_cycle_time

    def __str__(self):
        return f"Parameters(simulation_deep={self.simulation_deep}, working_time={self.working_time}, " \
               f"mobile_tank_volume={self.mobile_tank_volume}, vehicle_speed={self.vehicle_speed}, " \
               f"loading_time={self.loading_time}, pumping_speed={self.pumping_speed}, " \
               f"draining_speed={self.draining_speed}, percentage_volume_threshold={self.percentage_volume_threshold}, " \
               f"percentage_partial_collect_volume={self.percentage_partial_collect_volume}, " \
               f"minimum_draining_volume={self.minimum_draining_volume}, average_cycle_time={self.average_cycle_time})"

class Storehouse:
    def __init__(self, id: str, latitude: float, longitude: float, collector: str):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.collector = collector

    def __str__(self):
        return f"Storehouse(id={self.id}, latitude={self.latitude}, longitude={self.longitude}, collector={self.collector})"

class Agent:
    def __init__(self, id: str, name: str, surname: str, working_days: List[int], begin_hour: int):
        self.id = id
        self.name = name
        self.surname = surname
        self.working_days = working_days
        self.begin_hour = begin_hour

    def __str__(self):
        return f"Agent(id={self.id}, name={self.name}, surname={self.surname}, working_days={self.working_days}, begin_hour={self.begin_hour})"


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

    def __str__(self):
        return f"Tank ID: {self.id}, Name: {self.tank_name}, Barcode: {self.barcode}, " \
               f"Collector: {self.collector}, Status: {self.tank_status_label}, " \
               f"Current Volume: {self.current_volume}, Fill Level: {self.fill_level}"
    
class Maker:
    def __init__(self, keys_tanks, collector, ending_vacation, days, opening_vacation,
                 address, hours, country, name, post_code, city, internal_name,
                 longitude, id, latitude):
        self.keys_tanks = keys_tanks
        self.collector = collector
        self.ending_vacation = ending_vacation
        self.days = days
        self.opening_vacation = opening_vacation
        self.address = address
        self.hours = []
        for hour_range_str in ast.literal_eval(hours):
            hour_range_datetime = []
            for hour in hour_range_str:
                if hour == "24:00":
                    hour = "00:00"
                hour_range_datetime.append(datetime.strptime(hour, '%H:%M'))
            self.hours.append(hour_range_datetime)
        self.country = country
        self.name = name
        self.post_code = post_code
        self.city = city
        self.internal_name = internal_name
        self.longitude = longitude
        self.id = id
        self.latitude = latitude

    def __str__(self):
        return f"Maker(keys_tanks={self.keys_tanks}, collector={self.collector}, " \
               f"ending_vacation={self.ending_vacation}, days={self.days}, " \
               f"opening_vacation={self.opening_vacation}, address={self.address}, " \
               f"hours={self.hours}, country={self.country}, name={self.name}, " \
               f"post_code={self.post_code}, city={self.city}, " \
               f"internal_name={self.internal_name}, longitude={self.longitude}, " \
               f"id={self.id}, latitude={self.latitude})"
