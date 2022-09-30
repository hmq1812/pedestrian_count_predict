import numpy as np
import pandas as pd
import datetime as dt


def preprocess(ped_count, ped_loc):
    # Merge to dataset to get longitude and latitude of sensors
    ped_loc = ped_loc[['sensor_id', 'latitude', 'longitude']]
    ped_loc = ped_loc.rename(columns={'sensor_id': 'Sensor_ID', 'latitude': 'Latitude', 'longitude': 'Longitude'})
    ped_count = pd.merge(ped_count, ped_loc)
    ped_count = ped_count.drop(['ID','Date_Time', 'Sensor_Name', 'Sensor_ID'], axis=1)
    # ped_count['Month'] = pd.to_datetime(ped_count.Month, format='%B').dt.month # Convert month data from October to 10

    ped_count = ped_count.dropna()

    # Treat Year, Month, Mdata, Day and Time as discrete variables and perform 1 hot encoding for them
    # cat_vars = ['Month','Day']
    cat_vars = ['Year','Month','Mdate','Day','Time']
    for var in cat_vars:
        cat_list='var'+'_'+var
        cat_list = pd.get_dummies(ped_count[var], prefix=var)
        data1=ped_count.join(cat_list)
        ped_count=data1


    cat_vars = ['Year','Month','Mdate','Day','Time']
    # cat_vars = ['Month','Day']
    data_vars=ped_count.columns.values.tolist()
    to_keep=[i for i in data_vars if i not in cat_vars]

    # ped_count = ped_count.drop(['Month','Day'], axis=1)
    ped_count = ped_count.drop(['Year','Month','Mdate','Day','Time'], axis=1)

    # Move Hourly Counts to the last
    ped_count = ped_count[[c for c in ped_count if c not in ['Hourly_Counts']] + ['Hourly_Counts']]

    # Convert Hourly Count from string to int
    hr_count = []

    for x in ped_count['Hourly_Counts']:
        hr_count.append(int(x.replace(',', '')))


    hr_count_df = pd.DataFrame(hr_count, columns=['Hourly_Counts'])
    ped_count = ped_count.drop(['Hourly_Counts'], axis=1)
    ped_count = pd.concat([ped_count, hr_count_df], axis=1, join='inner')

    return ped_count