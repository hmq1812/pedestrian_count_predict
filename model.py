from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

def create_model():
    # Initialising the ANN
    model = Sequential()

    # Adding the input layer and the first hidden layer
    model.add(Dense(64, kernel_initializer='normal', input_dim = 90))

    # Adding the second hidden layer
    model.add(Dense(32, kernel_initializer='normal',activation='relu'))
    model.add(Dense(16, kernel_initializer='normal',activation='relu'))
    model.add(Dense(8, kernel_initializer='normal',activation='relu'))
    model.add(Dense(4, kernel_initializer='normal',activation='relu'))

    # Adding the output layer
    model.add(Dense(units = 1))

    return model

