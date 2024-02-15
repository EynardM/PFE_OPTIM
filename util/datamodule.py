from util.imports import * 
from util.objects import *
from util.locations import *
from util.helpers import *

def get_data() -> Tuple[List[Measurement], List[Tank], List[Maker]] :
    df_measurements = pd.read_csv(MEASUREMENTS_PATH)
    df_tanks = pd.read_csv(TANKS_PATH)
    df_makers = pd.read_csv(MAKERS_PATH)
    df_fillings_stats = pd.read_csv(FILLINGS_STATS_PATH)

    measurements = create_measurement_objects_from_dataframe(df_measurements)
    tanks = create_tank_objects_from_dataframe(df_tanks)
    makers = create_maker_objects_from_dataframe(df_makers)

    for tank in tanks: 
        tank_row = df_fillings_stats[df_fillings_stats['id'] == tank.id]
        if tank_row.empty:
            tank.mean_filling = np.mean(df_fillings_stats['mean_non_zeros'].iloc[0])
        else:
            tank.mean_filling = tank_row['mean_non_zeros'].iloc[0]
        for maker in makers:
            if tank.key_maker == maker.id:
                tank.maker = maker

    return measurements, tanks, makers