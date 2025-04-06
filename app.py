from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import datetime
import calendar


app = Flask(__name__)
model = load_model("receipt_model.keras")

#load last month of data from 2021 for janurary's prediction
df = pd.read_csv("data_daily.csv", names=["Date", "Receipt_Count"], skiprows=1, parse_dates=["Date"])
df = df.sort_values(by="Date")
df = df[df["Date"] < "2021-11-01"]
#scaler = MinMaxScaler()
#scaled_data = scaler.fit_transform(df["Receipt_Count"].values.reshape(-1, 1))
def normalize(data):
    min_val = np.min(data)
    max_val = np.max(data)
    return (data - min_val) / (max_val - min_val), min_val, max_val

def inverseNorm(data, nmax, nmin):
    return data*(nmax-nmin)+nmin

# Normalize data (train and test)
scaled_data, n_min, n_max = normalize(df["Receipt_Count"].values)

last_30_days = scaled_data[-30:]

#cache results of each month so we only need to compute each month once
cachepred = {};

@app.route("/", methods=["GET", "POST"])
def index():
    months = list(calendar.month_name)[1:]
    prediction_result = None

    if request.method == "POST":
        month_index = list(calendar.month_name).index(request.form["month"])

        year = 2022
        days_in_month = calendar.monthrange(year, month_index)[1]

        #hit
        if month_index in cachepred :
            #predicted_counts = scaler.inverse_transform(np.array(cachepred[month_index]).reshape(-1, 1)).flatten();
            predicted_counts = inverseNorm(np.array(cachepred[month_index]), n_max, n_min)
            dates = [datetime.date(year, month_index, day) for day in range(1, days_in_month + 1)]
            res = list(zip(dates, predicted_counts.astype(int)))

            return render_template("index.html", months=calendar.month_name[1:], prediction_result=res);

        predictions = []
        current_sequence = last_30_days.copy()

        #predict further in future by using past predictions
        #ex: march's result depends on feb's pred which depends on januaray's result
        for i in range(0, month_index):
            days_in_month = calendar.monthrange(year, i+1)[1];
            for _ in range(days_in_month):
                input_seq = current_sequence[-30:].reshape((1, 30, 1))
                next_day_scaled = model.predict(input_seq, verbose=0)
                predictions.append(next_day_scaled[0][0])
                current_sequence = np.append(current_sequence, next_day_scaled)[-30:]
            predictions = predictions[-31:]
            #cache after each month
            cachepred[i]=predictions;

        #predicted_counts = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
        predicted_counts = inverseNorm(np.array(predictions), n_max, n_min)

        #generate dates for table
        dates = [datetime.date(year, month_index, day) for day in range(1, days_in_month + 1)]

        prediction_result = list(zip(dates, predicted_counts.astype(int)))

    return render_template("index.html", months=calendar.month_name[1:], prediction_result=prediction_result)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)