from util.imports import * 
from util.objects import *
from util.locations import *
from util.helpers import *

def get_data() -> Tuple[List[Measurement], List[Tank], List[Maker]] :
    df_measurements = pd.read_csv(MEASUREMENTS_PATH)
    df_tanks = pd.read_csv(TANKS_PATH)
    df_makers = pd.read_csv(MAKERS_PATH)

    measurements = create_measurement_objects_from_dataframe(df_measurements)
    tanks = create_tank_objects_from_dataframe(df_tanks)
    makers = create_maker_objects_from_dataframe(df_makers)

    for tank in tanks: 
        for maker in makers:
            if tank.key_maker == maker.id:
                tank.maker = maker

    return measurements, tanks, makers