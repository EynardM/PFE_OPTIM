from util.imports import *

def colored(variable, color, variable_name=None, logs=True):
    """
    Print or log a colored representation of a variable.

    Args:
        variable: The variable to be displayed.
        color (str): The color to be applied (e.g., "red", "green", "bright_cyan").
        variable_name (str, optional): The name of the variable. If not provided, it is inferred from the calling frame.
        logs (bool, optional): If True, log the colored variable; otherwise, print to console. Default is True.
    """
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
        print("Unsupported color.")
        return

    color_code = color_map[color]
    reset_code = Style.RESET_ALL

    # Retrieve the variable name if not provided
    if variable_name is None:
        frame = inspect.currentframe().f_back
        variable_name = [name for name, value in frame.f_locals.items() if value is variable][0]

    if not logs:
        print(f"{color_code}{variable_name} = {variable}{reset_code}")
    else:
        logging.info(f"{color_code}{variable_name} = {variable}{reset_code}")

def make_empty(folder):
    """
    Empty the specified folder by deleting all its files.

    Args:
        folder (str): The path to the folder to be emptied.
    """
    
    files = os.listdir(folder)
    for file in files:
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
