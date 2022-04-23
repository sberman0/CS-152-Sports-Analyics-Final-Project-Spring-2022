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
# adjusted_list = team_list

col1, col2 = st.columns(2)
with col1:
    # fuck w the onchange thing
    your_team = st.selectbox('Select Your Team:', team_list)
                        #onchange=adjust_list(your_team, adjusted_list))
    
    if your_team != 'No Selection':
        st.write('You selected:', your_team)
        logo_filename = your_team + '-logo.png'
        logo = Image.open('images/' + logo_filename)
        cap = your_team + ' Logo'
        st.image(logo)

with col2:
    opponent = st.selectbox('Select Your Opponent:', team_list)

    if opponent != 'No Selection':
        st.write('You selected:', opponent)
        logo_filename2 = opponent + '-logo.png'
        logo2 = Image.open('images/' + logo_filename2)
        cap2 = opponent + ' Logo'
        st.image(logo2)
        


# if your_team != 'No Selection':
#     adjusted_list.remove(your_team)
# else:
#     adjusted_list = team_list



# if opponent != 'No Selection':
#     adjusted_list.remove(opponent)
# else:
#     adjusted_list = team_list

if your_team != 'No Selection':
    # st.write('You selected:', your_team)

    # get the your_team name and read in the data from the csv for that your_team
    filename = your_team + '_roster.csv'
    #st.write(filename)
    your_team_data = pd.read_csv('rosters/' + filename)
    your_team_players = your_team_data.Player

    # logo_filename = your_team + '-logo.png'
    # logo = Image.open('images/' + logo_filename)
    # cap = your_team + ' Logo'
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.write('')
    # with col2:
    #     st.image(logo)
    # with col3:
    #     st.write('')

    message1 = 'Select the players for the ' + your_team + ' lineup:'
    your_team_selected = st.multiselect(message1, your_team_players)

    st.write(your_team_selected)
    #st.write(options[0])

if opponent != 'No Selection':
    # st.write('You selected:', your_team)

    # get the your_team name and read in the data from the csv for that your_team
    filename2 = opponent + '_roster.csv'
    #st.write(filename)
    opponent_data = pd.read_csv('rosters/' + filename2)
    opponent_players = opponent_data.Player

    # logo_filename = opponent + '-logo.png'
    # logo = Image.open('images/' + logo_filename)
    # cap = opponent + ' Logo'
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.write('')
    # with col2:
    #     st.image(logo)
    # with col3:
    #     st.write('')

    message2 = 'Select the players for the ' + opponent + ' lineup:'
    opponent_selected = st.multiselect(message2, opponent_players)

    st.write(opponent_selected)
    #st.write(options[0])


