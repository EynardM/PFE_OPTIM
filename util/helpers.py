from util.imports import * 
from util.objects import *

def print_colored(variable, color, variable_name=None):
    color_map = {
        "blue": Fore.BLUE,
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "cyan": Fore.CYAN,
        "magenta": Fore.MAGENTA,
        "white": Fore.WHITE,
        "bright_black": Fore.BLACK + Style.BRIGHT,
        "bright_red": Fore.RED + Style.BRIGHT,
        "bright_green": Fore.GREEN + Style.BRIGHT,
        "bright_yellow": Fore.YELLOW + Style.BRIGHT,
        "bright_cyan": Fore.CYAN + Style.BRIGHT,
        "bright_magenta": Fore.MAGENTA + Style.BRIGHT,
        "bright_white": Fore.WHITE + Style.BRIGHT,
    }

    if color not in color_map:
        print("Couleur non supportée.")
        return

    color_code = color_map[color]
    reset_code = Style.RESET_ALL

    # Récupérer le nom de la variable si non fourni
    if variable_name is None:
        frame = inspect.currentframe().f_back
        variable_name = [name for name, value in frame.f_locals.items() if value is variable][0]

    print(f"{color_code}{variable_name} = {variable}{reset_code}")

def parse_config(filename: str):
    with open(filename, 'r') as file:
        config_data = json.load(file)

    # Créer les objets à partir des données du fichier JSON
    optimization_parameters = Parameters(**config_data['optimization_parameters'])
    storehouse = Storehouse(**config_data['storehouse'])
    agent = Agent(**config_data['agent'])

    print_colored(optimization_parameters, "yellow")
    print_colored(storehouse, "cyan")
    print_colored(agent, "magenta")

    return optimization_parameters, storehouse, agent

def create_maker_objects_from_dataframe(df):
    makers_list = []
    for index, row in df.iterrows():
        maker = Maker(
            row['keys_tanks'],
            row['collector'],
            row['ending_vacation'],
            row['days'],
            row['opening_vacation'],
            row['address'],
            row['hours'],
            row['country'],
            row['name'],
            row['post_code'],
            row['city'],
            row['internal_name'],
            row['longitude'],
            row['id'],
            row['latitude']
        )
        makers_list.append(maker)
    return makers_list

def create_tank_objects_from_dataframe(df):
    tanks_list = []
    for index, row in df.iterrows():
        tank = Tank(
            row['barcode'],
            row['collector'],
            row['overflow_capacity'],
            row['last_reading_date'],
            row['tank_type_label'],
            row['tank_type_id'],
            row['nominal_capacity'],
            row['container_type_label'],
            row['tank_name'],
            row['key_maker'],
            row['container_type_id'],
            row['tank_status_label'],
            row['current_volume'],
            row['id'],
            row['tank_status_id'],
            row['fill_level']
        )
        tanks_list.append(tank)
    return tanks_list

def create_measurement_objects_from_dataframe(df):
    measurement_list = []
    for index, row in df.iterrows():
        measurement = Measurement(
            row['id'],
            row['drainage'],
            row['event_type_id'],
            row['event_type_label'],
            row['fill_level'],
            row['filling'],
            row['key_maker'],
            row['key_tank'],
            row['measured_height'],
            row['measurement_date'],
            row['measurement_status_id'],
            row['measurement_status_label'],
            row['note_type_id'],
            row['note_type_label'],
            row['vidange'],
            row['volume']
        )
        measurement_list.append(measurement)
    return measurement_list