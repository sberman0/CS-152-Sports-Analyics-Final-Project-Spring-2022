import streamlit as st
import csv
import pandas as pd
from PIL import Image

def adjust_list(team, lst):
    lst.remove(team)

st.write("""
         ## Monte Carlo Simulations for Batting Order Optimization (Change Me Later)
         """)

team_list = ['No Selection', 'Amherst', 'Bates', 
             'Bowdoin', 'Colby', 'Hamilton', 'Middlebury', 
             'Trinity', 'Tufts', 'Wesleyan', 'Williams']
adjusted_list = team_list

# fuck w the onchange thing
your_team = st.selectbox('Select Your Team:', adjusted_list)
                         #onchange=adjust_list(your_team, adjusted_list))

if your_team != 'No Selection':
    adjusted_list.remove(your_team)
else:
    adjusted_list = team_list

opponent = st.selectbox('Select Your Opponent:', adjusted_list)

if opponent != 'No Selection':
    adjusted_list.remove(opponent)
else:
    adjusted_list = team_list

if your_team != 'No Selection':
    st.write('You selected:', your_team)

    # get the your_team name and read in the data from the csv for that your_team
    filename = your_team + '_roster.csv'
    #st.write(filename)
    your_team_data = pd.read_csv('rosters/' + filename)
    players = your_team_data.Player

    logo_filename = your_team + '-logo.png'
    logo = Image.open('images/' + logo_filename)
    cap = your_team + ' Logo'
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('')
    with col2:
        st.image(logo)
    with col3:
        st.write('')

    options = st.multiselect('Select the players in the lineup', players)

    st.write(options)
    #st.write(options[0])


