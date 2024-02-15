from util.imports import *

def colored(variable, color, variable_name=None, logs=True):
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

    if not logs:
        print(f"{color_code}{variable_name} = {variable}{reset_code}")
    else :
        logging.info(f"{color_code}{variable_name} = {variable}{reset_code}")

def make_empty(folder):
    fichiers = os.listdir(folder)
    for fichier in fichiers:
        chemin_fichier = os.path.join(folder, fichier)
        if os.path.isfile(chemin_fichier):
            os.remove(chemin_fichier)