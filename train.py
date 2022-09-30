import numpy as np
import pandas as pd

import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from tensorflow.keras.callbacks import ModelCheckpoint

from reduce_ram_usage import import_data
from preprocessing import preprocess
from model import create_model
import config

def main():
    # ped_count = import_data(config.count_data)
    # ped_loc = import_data(config.sensor_data)
    ped_count = pd.read_csv(config.count_data)
    ped_loc = pd.read_csv(config.sensor_data)

    # Preprocess data
    ped_count = preprocess(ped_count, ped_loc)

    # Scale value
    sc = StandardScaler()
    ped_count_longlat = sc.fit_transform(ped_count.loc[:, ['Latitude',	'Longitude']])
    ped_count = ped_count.drop(['Latitude',	'Longitude'], axis=1)

    ped_count = np.concatenate([ped_count_longlat, ped_count], axis=1)

    # Save the scaler file
    joblib.dump(sc, config.scaler_path, compress=True)
    # Split train test
    X = ped_count[:, 0:90]
    y = ped_count[:, 90]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Create model and train
    model = create_model()

    checkpoint_name = 'model_data/Weights-{epoch:03d}--{val_loss:.5f}.hdf5' 
    checkpoint = ModelCheckpoint(checkpoint_name, monitor='val_loss', verbose = 1, save_best_only = True, mode ='auto')
    callbacks_list = [checkpoint]

    model.compile(optimizer = 'adam',loss = 'mean_squared_error', metrics=['accuracy'])

    model.fit(X_train, y_train, validation_split=0.25, batch_size = 32, epochs = 50, callbacks=[callbacks_list], verbose=1)


if __name__ == "__main__":
    main()