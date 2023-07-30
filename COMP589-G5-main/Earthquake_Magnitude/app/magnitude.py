# importing essential libraries
import numpy as np
from memory_profiler import profile
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
import time
import joblib
from app import DataPreprocessing


def MLClassifier(user_date, user_time, user_lat, user_long):
    # start2 = time.time()
    DataPreprocessing.data_preprocessing()  # '01/04/2021', '21:04:23', 34.024212, -118.496475
    # print("\nTime taken for Data Preprocessing Module to run: --- %.2f seconds --- " % (time.time() - start2))

    # start2 = time.time()
    training_model()
    # print("\nTime taken for ML Training Module to run: --- %.2f seconds --- " % (time.time() - start2))

    # start2 = time.time()
    result = prediction_model(user_date, user_time, user_lat, user_long)
    # print("\nTime taken for ML Prediction Module to run: --- %.2f seconds --- " % (time.time() - start2))

    # print("Classification completed")

    return result


# function to append the timestamp column
def create_timestamp():
    # reading the dataset for training
    dataset = pd.read_csv("../Dataset/PreprocessedEarthquakesDataset.csv")

    # creating the data_frame to be used for training with only essential columns
    data_frame = dataset.copy()
    timestamp = []

    for d, t in zip(dataset['Date'], dataset['Time']):

        try:
            timestamp_val = str(d) + " " + str(t)
            ts = datetime.datetime.strptime(timestamp_val, '%m/%d/%Y %H:%M:%S.%f')

            epoch = datetime.datetime.strptime("1/1/1970 0:0:0.0", '%m/%d/%Y %H:%M:%S.%f')
            diff = ts - epoch
            timestamp.append(diff.total_seconds())

        except ValueError:
            timestamp.append('ValueError')

    timeStamp = pd.Series(timestamp)
    data_frame.insert(6, 'Timestamp', timeStamp, allow_duplicates=True)

    return data_frame


# @profile
# function to create the training model
def training_model():
    df = pd.DataFrame(create_timestamp())

    final_dataset = df.loc[:, ~df.columns.isin(['Date', 'Time'])]
    final_dataset = final_dataset[final_dataset.Timestamp != 'ValueError']

    X = final_dataset[['Timestamp', 'Latitude', 'Longitude']]
    # print(X.head)
    y = final_dataset[['Magnitude', 'Depth']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    reg = RandomForestRegressor(random_state=42)
    reg.fit(X_train, y_train)

    # save model
    joblib.dump(reg, 'SavedRandomForestModel.joblib')

    # print("Training completed")


# @profile
def prediction_model(user_date, user_time, user_lat, user_long):
    model = joblib.load('SavedRandomForestModel.joblib')

    d1 = str(user_date)
    t1 = str(user_time + ':00')
    timestamp_val1 = (d1 + " " + t1)
    ts1 = datetime.datetime.strptime(timestamp_val1, '%m/%d/%Y %H:%M:%S')
    timestamp1 = time.mktime(ts1.timetuple())

    user_inp_data = pd.DataFrame({"Timestamp": [timestamp1], "Latitude": [user_lat], "Longitude": [user_long]})
    # print(user_inp_data.head)
    # user_inp_data = pd.DataFrame({"Latitude": [input_lat], "Longitude": [input_long]})
    # predicted_value = np.char.split(np.array2string(model.predict(user_inp_data)).replace("[", "").replace("]", ""))
    predicted_value = model.predict(user_inp_data)
    # print(magnitude_output, depth_output)
    # print('Predicted Magnitude and Depth', predicted_value)
    return predicted_value
