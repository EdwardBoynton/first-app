## Importing libraries 
import streamlit as st
import pandas as pd
import numpy as np

## Writing title
st.title('Uber pickups in NYC')

## Fetching Data
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

## Putting data on a cache for improved performance 
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower() ## takes input and lowercases
    data.rename(lowercase, axis='columns', inplace=True) ## Lowercasing columns 
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN]) ##Converting data to date/time object
    return data

## Text while loading
data_load_state = st.text('Loading data...')

## Assigning data to vairable 'data'
data = load_data(10000)

## Text once loaded
data_load_state.text("Done! (using st.cache_data)")

## Stressful morning 
st.write('An unoriginal app based off the Streamlit example as I spent too long trying to figure out how to run it in the first place. \#Silly \#me')

## Giving user option to see raw data 
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

## Giving user option to see Histogram of pick ups by hour
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
if st.checkbox('Show number of pickups by hour'):
    st.subheader('Number of pickups by hour')
    st.bar_chart(hist_values)

## Giving user option to see map of pickups per hour 
if st.checkbox('Show map of pickups by hour'):
    hour_to_filter = st.slider('hour', 0, 23, 0)  ## Creating a slider for the user to pick an hour from
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]  ## filtering data based on slider input
    st.subheader(f'Map of all pickups at {hour_to_filter}:00') ## Creating subheading that adjusts with slider input 
    st.map(filtered_data)