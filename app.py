from flask import Flask
from flask_ngrok import run_with_ngrok
from flask import request
from predict import Model

app = Flask(__name__)
# Using ngrok to create tunnel between internet and localhost
run_with_ngrok(app)
model = Model()

@app.route('/pred_pedestrian', methods = ['POST'])
def predict():
    if request.method == 'POST':
        try:
            try:
                # Required field in data form send to the API
                data = request.form # a multidict containing POST data
                lat = float(data['latitude'])
                long = float(data['longitude'])
                mdate = int(data['mdate'])
                month = int(data['month'])
                year = int(data['year'])
                time = int(data['time'])
                # Validate input
                if not (0 < mdate < 32 and 0 < month < 13 and 2000 < year < 2030 and -1 < time < 24):
                    return {"errorCode": 1, "errorMessage": "Input data value invalid"}, 400
            except:
                return {"errorCode": 1, "errorMessage": "Input data type invalid"}, 400
            # Call the model to predict on input data
            hr_count = model.predict(lat, long, mdate, month, year, time)

            return {"Predicted number of Pedestrian": hr_count}
        except:
            return {"errorCode": 2, "errorMessage": "Model could not predict value for given data"}, 400

if __name__ == "__main__":
    app.run()
