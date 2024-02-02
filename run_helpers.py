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

def find_first_available_time(tanks):
    # Initialiser une liste pour stocker toutes les heures de début des créneaux horaires
    all_start_times = []

    # Parcourir chaque réservoir
    for tank in tanks:
        # Parcourir chaque plage horaire du fabricant du réservoir
        for hour_range in tank.maker.hours:
            # Ajouter l'heure de début de chaque plage horaire à la liste
            all_start_times.append(hour_range[0])

    # Filtrer les heures de début après minuit
    after_midnight_times = [start_time for start_time in all_start_times if start_time.time() > datetime.strptime('00:00', '%H:%M').time()]

    # Trier les heures de début après minuit par ordre croissant
    sorted_after_midnight_times = sorted(after_midnight_times)

    # Retourner la première heure disponible après minuit
    if sorted_after_midnight_times:
        return sorted_after_midnight_times[0]
    else:
        return None