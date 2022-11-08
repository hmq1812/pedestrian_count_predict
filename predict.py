from cProfile import run
import datetime
from pickletools import read_uint1
from tensorflow.keras.models import load_model
import joblib
import pandas as pd
import datetime
import calendar
import time

import config

class Model(object):
    def __init__(self):
        # load model
        self.model = load_model(config.model_path)
        # load standard scaler
        self.sc=joblib.load(config.scaler_path)

    def predict(self, lat, long, mdate, month, year, time):
        # Standardize data
        data = self.transform_data(lat, long, mdate, month, year, time )
        return int(self.model.predict(data)[0][0])


    def transform_data(self, lat, long, mdate, month, year, time):
        my_date = datetime.date(year, month, mdate)
        day = calendar.day_name[my_date.weekday()]  #'Wednesday'
        # Create df for test data point
        data = pd.DataFrame([[0.0]*2 + [0]*88], columns=
        ['Latitude', 'Longitude', 'Year_2009', 'Year_2010', 'Year_2011',
        'Year_2012', 'Year_2013', 'Year_2014', 'Year_2015', 'Year_2016',
        'Year_2017', 'Year_2018', 'Year_2019', 'Year_2020', 'Year_2021',
        'Year_2022', 'Month_April', 'Month_August', 'Month_December',
        'Month_February', 'Month_January', 'Month_July', 'Month_June',
        'Month_March', 'Month_May', 'Month_November', 'Month_October',
        'Month_September', 'Mdate_1', 'Mdate_2', 'Mdate_3', 'Mdate_4',
        'Mdate_5', 'Mdate_6', 'Mdate_7', 'Mdate_8', 'Mdate_9', 'Mdate_10',
        'Mdate_11', 'Mdate_12', 'Mdate_13', 'Mdate_14', 'Mdate_15', 'Mdate_16',
        'Mdate_17', 'Mdate_18', 'Mdate_19', 'Mdate_20', 'Mdate_21', 'Mdate_22',
        'Mdate_23', 'Mdate_24', 'Mdate_25', 'Mdate_26', 'Mdate_27', 'Mdate_28',
        'Mdate_29', 'Mdate_30', 'Mdate_31', 'Day_Friday', 'Day_Monday',
        'Day_Saturday', 'Day_Sunday', 'Day_Thursday', 'Day_Tuesday',
        'Day_Wednesday', 'Time_0', 'Time_1', 'Time_2', 'Time_3', 'Time_4',
        'Time_5', 'Time_6', 'Time_7', 'Time_8', 'Time_9', 'Time_10', 'Time_11',
        'Time_12', 'Time_13', 'Time_14', 'Time_15', 'Time_16', 'Time_17',
        'Time_18', 'Time_19', 'Time_20', 'Time_21', 'Time_22', 'Time_23'])

        # Mark value in df
        data.at[0,'Year_'+str(year)]=1
        data.at[0,'Month_'+my_date.strftime("%B")]=1
        data.at[0,'Mdate_'+str(mdate)]=1
        data.at[0,'Day_'+str(day)]=1
        data.at[0,'Time_'+str(time)]=1

        # Scale lat and long data
        latlong_scaled = self.sc.transform(pd.DataFrame([[lat, long]], columns=
        ['Latitude', 'Longitude']))
        data.at[0,'Latitude']=latlong_scaled[0,0]
        data.at[0,'Longitude']=latlong_scaled[0,1]

        return data


if __name__ == "__main__":
    m = Model()
    start_time = time.time()
    print(m.predict(-37.81766034, 144.95026189, 2, 3, 2020, 12))
    print("Result produced in --- %s seconds ---" % (time.time() - start_time))


    start_time = time.time()
    print(m.predict(-37.81766034, 144.95026189, 2, 3, 2020, 16))
    print("Result produced in --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    print(m.predict(-37.81766034, 144.95026189, 2, 3, 2020, 2))
    print("Result produced in --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    print(m.predict(-37.81766034, 144.95026189, 2, 3, 2020, 9))
    print("Result produced in --- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    print(m.predict(-37.81766034, 144.95026189, 2, 3, 2020, 21))
    print("Result produced in --- %s seconds ---" % (time.time() - start_time))