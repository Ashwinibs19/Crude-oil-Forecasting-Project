# -*- coding: utf-8 -*-
"""Forecast_Crude_oil_Deployment-1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KpjuN480XpkO3K1spApmRIdhPa_WPE_4
"""

import pickle
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import calendar
from math import sqrt
import datetime
import warnings
warnings.filterwarnings("ignore")

#load the model
model = pickle.load(open('forecast_model.pickle','rb'))

#load dataset to plot alongside predictions
df1 = pd.read_csv("EuropeanBrent.csv")
df1['Date']=pd.to_datetime(df1['Date'],format='mixed')
df2=df1.set_index('Date').resample('M').mean()
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(df2)
look_back = 1

#page configuration
st.set_page_config(layout='centered')
image = Image.open('header.jpg')
st.image(image)

num_prediction = st.slider("Select number of Months",1,36,step = 1)

dataset1 = dataset.reshape((-1))

def predict(num_prediction, model):
    prediction_list = dataset[-look_back:]

    for _ in range(num_prediction):
        x = prediction_list[-look_back:]
        x = x.reshape((1, look_back, 1))
        out = model.predict(x)[0][0]
        prediction_list = np.append(prediction_list, out)
    prediction_list = prediction_list[look_back-1:]

    return prediction_list

def predict_dates(num_prediction):
    last_date = df2.index.values[-1]
    prediction_dates = pd.date_range(last_date, periods=num_prediction+1,freq='M').tolist()
    return prediction_dates
forecast = predict(num_prediction, model)
forecast_dates = predict_dates(num_prediction)
forecast=forecast.reshape(-1,1)
forecast = scaler.inverse_transform(forecast)
forecast_dates=pd.to_datetime(forecast_dates)
forecasted_data_final=pd.DataFrame()
forecasted_data_final['Date']=forecast_dates
forecasted_data_final['Oil_Price']=forecast
forecasted_data_final.drop(index=0,inplace=True)
forecasted_data_final.set_index('Date', inplace=True)
st.subheader('Predicted Result')

if st.button("Predict"):

        col1, col2 = st.columns([2,3])
        with col1:
             st.dataframe(forecasted_data_final)
        with col2:
           st.write("Trend & Forecast of Crude oil Price")
           fig, ax = plt.subplots()
           plt.plot(df2, label='Original')
           plt.plot(forecasted_data_final, label='Forecast')
           plt.legend(loc='best')
           st.pyplot(fig)
