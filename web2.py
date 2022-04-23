import streamlit as st
import csv
import pandas as pd
from PIL import Image

st.write("""
         ## Monte Carlo Simulations for Batting Order Optimization (Change Me Later)
         """)

team = st.selectbox('Select a team:', ['No Selection', 'Amherst', 'Bates', 
                    'Bowdoin', 'Colby', 'Conn. College', 'Hamilton',
                    'Middlebury', 'Trinity', 'Tufts', 'Wesleyan', 'Williams'])

if team != 'No Selection':
    st.write('You selected:', team)

    # get the team name and read in the data from the csv for that team
    filename = team + "_roster.csv"
    st.write(filename)
    team_data = pd.read_csv(filename)
    players = team_data.Name

if team == 'Tufts':
    logo = Image.open('images/tufts-logo.png')
    st.image(logo, caption='Tufts Logo')

    options = st.multiselect('Select the players in the lineup', players)

    st.write(options)
    #st.write(options[0])


