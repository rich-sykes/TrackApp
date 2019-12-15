import pandas as pd
import re

# example string for lap sector
# line = "\n\t\t\t00:35.10,1116.4\n\t\t\t02:23.01,5093.0\n\t\t\t04:26.63,9444.4\n\t\t\t06:58.61,14396.5\n\t\t"

def convert_sector_string(string, lap_index):

    line = re.sub('\t', '', string)
    line = line.split("\n")
    my_list = [item.split(",") for item in line if item != '']

    df = pd.DataFrame.from_records(my_list, columns=['Time', 'Distance'])
    df['Lap'] = float(lap_index)
    df['Time'] = pd.to_datetime(df['Time'], format='%M:%S.%f').dt.time
    df['Distance'] = df['Distance'].astype(float)

    df['Sector'] = df.index.values + 1

    return df
