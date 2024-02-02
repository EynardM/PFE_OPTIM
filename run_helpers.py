from util.imports import * 
from util.objects import *

def filter_days(tanks : List[Tank]) -> List[Tank]:
    now = datetime.now()
    day = now.strftime("%A")
    day_index = {calendar.day_name[i]: i for i in range(7)}[day]

    tanks_filtered_by_days = []
    for tank in tanks:
        if tank.maker.days[day_index] == "1":
            tanks_filtered_by_days.append(tank)
    return tanks_filtered_by_days

def filter_quantities(tanks : List[Tank], parameters: Parameters) -> List[Tank]:
    tanks_filtered_by_quantity = []
    for tank in tanks: 
        if tank.current_volume / tank.overflow_capacity >= parameters.percentage_volume_threshold:
            tanks_filtered_by_quantity.append(tank)
    return tanks_filtered_by_quantity

def get_start_hour(tanks: List[Tank], agent: Agent):
    print(agent.begin_hour)
    all_start_times = []
    for tank in tanks:
        for hour_range in tank.maker.hours:
            all_start_times.append(hour_range[0])
    after_midnight_times = [start_time for start_time in all_start_times if start_time.time() > datetime.strptime('00:00', '%H:%M').time()]
    sorted_after_midnight_times = sorted(after_midnight_times)
    if sorted_after_midnight_times:
        return max(sorted_after_midnight_times[0], agent.begin_hour)
    else:
        return None