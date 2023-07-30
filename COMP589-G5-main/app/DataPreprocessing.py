# import libraries
import pandas as pd
import os


# from memory_profiler import profile


# @profile
def data_cleaning(earth_data):
    # # Data Analysis of data set

    # # Determine if there are any missing values
    # print(earth_data.isna().sum())

    # # # info on data types
    # print(earth_data.info())

    # # # Data insight
    # print(earth_data.describe())

    # # # Number of columns and rows in data set
    # print(earth_data.shape)

    # Combine Data columns (year, month, day) and Time()
    earth_data['Date'] = earth_data[earth_data.columns[4:6]].apply(lambda x: ' ', axis=1)
    earth_data['Date'] = earth_data['month'].astype(str) + "/" + earth_data['day'].astype(str) + "/" + earth_data[
        'year'].astype(str)

    # Combine Time columns ( hour, minute, seconds)
    cols = earth_data[earth_data.columns[7:9]]
    earth_data['Time'] = cols.apply(lambda x: ':'.join(x.values.astype(str)), axis=1)
    earth_data['Time'] = earth_data['hour'].astype(str) + ":" + earth_data['minute'].astype(str) + ":" + earth_data[
        'second'].astype(str)

    # Data for analysis
    earth_df = earth_data[['Date', 'Time', 'Mw', 'long_degE', 'lat_degN', 'depth_km']]
    earth_df.columns = ['Date', 'Time', 'Magnitude', 'Longitude', 'Latitude', 'Depth']
    # earth_df.rename(
    #     columns={"Date": "Date", "Time": "Time", "Mw": "Magnitude", "long_degE": "Longitude", "lat_degN": "Latitude",
    #              "depth_km": "Depth"}, inplace=True)

    # print(earth_df.head())
    #
    # # Determine data types
    # print(earth_df.info())
    #
    # # Determine the number of zeros in the depth column
    # print(earth_df['Depth'].value_counts()[0])
    #
    # print(earth_df.isna().sum())

    # appending kaggle data to dataframe
    significant_earth_df = pd.read_csv("../Dataset/SignificantEarthquakesDataset.csv")
    significant_earth_df = significant_earth_df[['Date', 'Time', 'Magnitude', 'Longitude', 'Latitude', 'Depth']]

    earth_df_combined = pd.concat([earth_df, significant_earth_df], ignore_index=True)
    # print(earth_df_combined.info())

    return earth_df_combined


# @profile
def data_preprocessing():
    # read data from file
    earth_data = pd.read_csv("Dataset/eqcat_CEUS1568-2018.csv")
    clean_data = data_cleaning(earth_data)
    clean_data.to_csv("Dataset/PreprocessedEarthquakesDataset.csv", index=False)
