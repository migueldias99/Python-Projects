import streamlit as st
import pandas as pd
import numpy as np

#Following an example given by Stremlit website, this is used to analyse the data of uber pickups in NYC
st.title('Uber pickups in NYC')
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
#@st.cache_data
#cache can be used, to avoid wasting time loading the data (check https://docs.streamlit.io/get-started/tutorials/create-an-app for more info)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done!")
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)
st.subheader('Number of pickups by hour')
#histogram values, for the number of pickups by hour in NYC
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)
#plot the pickups on a map
st.subheader('Map of all pickups')
st.map(data)
#Show the map for one specific hour
#hour_to_filter = 17
#Filter the results using a slider, instead of defining the hour as a variable
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)