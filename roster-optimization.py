# 
# CS 152: Sports Analytics
# Spring 2022
# Final Project
# NESCAC Baseball Batting Order Optimization
#
# Authors: Samuel Berman       (sberma04)
#          Alex Maleno         (amalen01)
#          Thomas "Clay" Kynor (tkynor01)
#
# Purpose: A Streamlit web application that allows users
#          to select a NESCAC team and a list of players from
#          that team. Program them runs a Monte Carlo simulation
#          of those players to determine the average number of
#          runs that batting lineup would score.
#

# from audioop import avg
# from pydoc import tempfilepager
# from sys import orig_argv
from webbrowser import get
import streamlit as st
import csv
import pandas as pd
from PIL import Image
#import re, math
import random
from itertools import permutations
import time



#
# Utility Functions
#

def read_team_data(data):
    # team_data = pd.read_csv(filename)
    df = pd.DataFrame(data)

    return df

# --------------------------------------------------------- #
#                calculate_thresholds()
#
#  Calculate the thresholds for the Monte Carlo Simulation
#
#  Creates a dictionary where the key is the threshold type
#  (ex: outs, 1B, BB, etc.) and the values are a list of
#  thresholds for each player in the lineup.
#  The keys are the following:
#
#       outs, strikeouts, HBP, BB, 1B, 2B, 3B, HR
#
#  Note: We don't have access to errors with the NESCAC data
#        so we are ignoring that value.
#
# --------------------------------------------------------- #
def calculate_thresholds(df, players):
    df['1B'] = 0
    thresholds = {}
    for i, row in df.iterrows():

        # add singles into data frame b/c NESCAC doesn't have it
        df['1B'][i] = df['H'][i] - df['2B'][i] - df['3B'][i] - df['HR'][i]

        # find the thresholds
        curr_threshold = 0
        if df['Player'][i] not in players:
            continue
        
        at_bats = df['AB'][i]
        outs = (df['AB'][i] - df['H'][i] - df['BB'][i] - df['HBP'][i] - df['SO'][i])
        curr_threshold = outs / at_bats
        if 'out_thresh' not in thresholds.keys():
            thresholds['out_thresh'] = [curr_threshold]
        else:
            thresholds['out_thresh'].append(curr_threshold)

        curr_threshold += df['SO'][i] / at_bats
        if 'so_thresh' not in thresholds.keys():
            thresholds['so_thresh'] = [curr_threshold]
        else:
            thresholds['so_thresh'].append(curr_threshold)

        curr_threshold += df['HBP'][i] / at_bats
        if 'hbp_thresh' not in thresholds.keys():
            thresholds['hbp_thresh'] = [curr_threshold]
        else:
            thresholds['hbp_thresh'].append(curr_threshold)

        curr_threshold += df['BB'][i] / at_bats
        if 'bb_thresh' not in thresholds.keys():
            thresholds['bb_thresh'] = [curr_threshold]
        else:
            thresholds['bb_thresh'].append(curr_threshold)

        curr_threshold += df['1B'][i] / at_bats
        if '1b_thresh' not in thresholds.keys():
            thresholds['1b_thresh'] = [curr_threshold]
        else:
            thresholds['1b_thresh'].append(curr_threshold)

        curr_threshold += df['2B'][i] / at_bats
        if '2b_thresh' not in thresholds.keys():
            thresholds['2b_thresh'] = [curr_threshold]
        else:
            thresholds['2b_thresh'].append(curr_threshold)

        curr_threshold += df['3B'][i] / at_bats
        if '3b_thresh' not in thresholds.keys():
            thresholds['3b_thresh'] = [curr_threshold]
        else:
            thresholds['3b_thresh'].append(curr_threshold)

        curr_threshold += df['HR'][i] / at_bats
        if 'hr_thresh' not in thresholds.keys():
            thresholds['hr_thresh'] = [curr_threshold]
        else:
            thresholds['hr_thresh'].append(curr_threshold)

    return thresholds


def run_monte_carlo(thresholds):

    game_state = dict({'1B': 0, '2B': 0, '3B':0, 'Outs': 0, 'Runs':0, 'Next_Batter':0, 'Inning':1})

    for i in range(1,10):
        # For each inning, reset the out count and bases
        game_state['Outs'] = 0
        game_state['1B'] = 0
        game_state['2B'] = 0
        game_state['3B'] = 0
        
        while (game_state['Outs'] < 3):

            rand = (random.randint(1,10000))/10000.0

            # Batter gets out
            if (rand < thresholds['out_thresh'][game_state['Next_Batter']]):
                game_state['Outs'] += 1

            # Strikeout
            elif (rand < thresholds['so_thresh'][game_state['Next_Batter']]):
                game_state['Outs'] += 1

            # HBP
            elif (rand < thresholds['hbp_thresh'][game_state['Next_Batter']]):
                if game_state['1B'] == 1:
                    if game_state['2B'] == 1:
                        if game_state['3B'] == 1:
                            game_state['Runs'] += 1
                        else:
                            game_state['3B'] = 1
                    else:
                        game_state['2B'] = 1
                else:
                    game_state['1B'] = 1

            # Walks
            elif (rand < thresholds['bb_thresh'][game_state['Next_Batter']]):
                if game_state['1B'] == 1:
                    if game_state['2B'] == 1:
                        if game_state['3B'] == 1:
                            game_state['Runs'] += 1
                        else:
                            game_state['3B'] = 1
                    else:
                        game_state['2B'] = 1
                else:
                    game_state['1B'] = 1

            # Singles
            elif (rand < thresholds['1b_thresh'][game_state['Next_Batter']]):
                if game_state['1B'] == 1:
                    if game_state['2B'] == 1:
                        if game_state['3B'] == 1:
                            game_state['Runs'] += 1
                        else:
                            game_state['3B'] = 1
                    else:
                        game_state['2B'] = 1
                else:
                    game_state['1B'] = 1

            # Doubles
            # Note: Assumes all runners get 2 bases
            elif (rand < thresholds['hbp_thresh'][game_state['Next_Batter']]):
                if game_state['3B'] == 1:
                    game_state['Runs'] += 1
                    game_state['3B'] = 0
                
                if game_state['2B'] == 1:
                    game_state['Runs'] += 1
                    game_state['2B'] = 0

                if game_state['1B'] == 1:
                    game_state['1B'] = 0
                    game_state['3B'] = 1

                game_state['2B'] = 1

            # Triples
            # Note: Assumes all runners get 3 bases
            elif (rand < thresholds['hbp_thresh'][game_state['Next_Batter']]):
                if game_state['3B'] == 1:
                    game_state['Runs'] += 1
                    game_state['3B'] = 0
                
                if game_state['2B'] == 1:
                    game_state['Runs'] += 1
                    game_state['2B'] = 0

                if game_state['1B'] == 1:
                    game_state['Runs'] += 1
                    game_state['1B'] = 0

                game_state['3B'] = 1

            # Home runs
            else:
                game_state['Runs'] += game_state['3B']
                game_state['Runs'] += game_state['2B']
                game_state['Runs'] += game_state['1B']
                game_state['1B'] = 0
                game_state['2B'] = 0
                game_state['3B'] = 0
                game_state['Runs'] += 1

            game_state['Next_Batter'] = (game_state['Next_Batter'] + 1) % (len(thresholds['1b_thresh']))

    return game_state['Runs']

def avg_runs(thresholds):
    runs = []
    for i in range(1000):
        runs.append(run_monte_carlo(thresholds))

    return (sum(runs) / len(runs))

def flip(players, i, j):
    players[i], players[j] = players[j], players[i]
    return players

def do_flip_optimization(df, players):
    curr_players = players[:]
    thresholds = calculate_thresholds(df, curr_players)
    best_runs = avg_runs(thresholds)
    best_lineup = curr_players
    
    for i in range(len(players) - 2): # - 1 so we can flip the end w/o OOB
        curr_players = flip(players[:], i, i + 1)
        thresholds = calculate_thresholds(df, curr_players)
        runs = avg_runs(thresholds)

        if runs > best_runs:
            best_runs = runs
            best_lineup = curr_players

    return best_lineup, best_runs

def check_file(data):
    # make sure the appropriate columns exist
    cols = ['Player', 'AB', 'SO', 'HBP', 'BB', '2B', '3B', 'HR']
    for col in cols:
        if col not in data.columns:
            return False

    # make sure there are at least 9 players
    if len(data.index) < 9:
        return False

    return True

def get_new_data():
    uploaded_file = st.file_uploader("Upload a new csv data file", type='csv')
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        return dataframe


def run_compare_lineups(your_team_players, data):
    col1, col2 = st.columns(2)
    with col1:
        st.write('#### Select the players for lineup 1:')
        one   = st.selectbox('Lead-Off: ', your_team_players)
        two   = st.selectbox('Second: ', your_team_players)
        three = st.selectbox('Third: ', your_team_players)
        four  = st.selectbox('Clean Up: ', your_team_players)
        five  = st.selectbox('Fifth: ', your_team_players)
        six   = st.selectbox('Sixth: ', your_team_players)
        seven = st.selectbox('Seventh: ', your_team_players)
        eight = st.selectbox('Eighth: ', your_team_players)
        nine  = st.selectbox('Ninth: ', your_team_players)
    with col2:
        st.write('#### Select the players for lineup 2:')
        one2   = st.selectbox('Lead-Off:  ', your_team_players)
        two2   = st.selectbox('Second:  ', your_team_players)
        three2 = st.selectbox('Third:  ', your_team_players)
        four2  = st.selectbox('Clean Up:  ', your_team_players)
        five2  = st.selectbox('Fifth:  ', your_team_players)
        six2   = st.selectbox('Sixth:  ', your_team_players)
        seven2 = st.selectbox('Seventh:  ', your_team_players)
        eight2 = st.selectbox('Eighth:  ', your_team_players)
        nine2  = st.selectbox('Ninth:  ', your_team_players)

    if st.button('Submit'):
        lineup1 = [one, two, three, four, five, six, seven, eight, nine]
        lineup2 = [one2, two2, three2, four2, five2, six2, seven2, eight2, nine2]
        
        players_set1 = set(lineup1)
        players_set2 = set(lineup2)

        if '<select>' in players_set1 or '<select>' in players_set2:
            st.error('Select a player for each position in the lineup')
        elif len(players_set1)!= 9 or len(players_set2) != 9:
            st.error('No duplicates allowed')
        elif lineup1 == lineup2:
            st.error('Lineups cannot be the same')
        else:
            df = read_team_data(data)

            thresh1 = calculate_thresholds(df, lineup1)
            thresh2 = calculate_thresholds(df, lineup2)
            avg1 = avg_runs(thresh1)
            avg2 = avg_runs(thresh2)

            st.write("""## Better Lineup:""")
            if avg1 > avg2:
                st.write("Lineup #1")
                st.write(lineup1)
            else:
                st.write("Lineup #2")
                st.write(lineup2)

def run_predicted_runs(your_team_players, data, team_name):
    st.write(' ### Select the players for the ' + team_name + ' lineup:')

    col1, col2 = st.columns(2)
    with col1:
        one = st.selectbox('Lead-Off: ', your_team_players)
        three = st.selectbox('Third: ', your_team_players)
        five = st.selectbox('Fifth: ', your_team_players)
        seven = st.selectbox('Seventh: ', your_team_players)
        nine = st.selectbox('Ninth: ', your_team_players)
    with col2:
        two = st.selectbox('Second: ', your_team_players)
        four = st.selectbox('Clean Up: ', your_team_players)
        six = st.selectbox('Sixth: ', your_team_players)
        eight = st.selectbox('Eighth: ', your_team_players)

    if st.button('Submit'):
        lineup = [one, two, three, four, five, six, seven, eight, nine]
        lineup_set = set(lineup)

        if '<select>' in lineup_set:
            st.error('Select a player for each position in the lineup')
        elif len(lineup_set) != 9:
            st.error('No duplicates allowed')
        else:
            df = read_team_data(data)
        
            thresholds = calculate_thresholds(df, lineup)
            st.title("Number of predicted runs: " + str(avg_runs(thresholds)))
            

def run_lineup_optimization(your_team_players, data, team_name):
    st.write(' ### Select the players for the ' + team_name + ' lineup:')

    col1, col2 = st.columns(2)
    with col1:
        one = st.selectbox('Lead-Off: ', your_team_players)
        three = st.selectbox('Third: ', your_team_players)
        five = st.selectbox('Fifth: ', your_team_players)
        seven = st.selectbox('Seventh: ', your_team_players)
        nine = st.selectbox('Ninth: ', your_team_players)
    with col2:
        two = st.selectbox('Second: ', your_team_players)
        four = st.selectbox('Clean Up: ', your_team_players)
        six = st.selectbox('Sixth: ', your_team_players)
        eight = st.selectbox('Eighth: ', your_team_players)

    if st.button('Submit'):
        lineup = [one, two, three, four, five, six, seven, eight, nine]
        lineup_set = set(lineup)

        if '<select>' in lineup_set:
            st.error('Select a player for each position in the lineup')
        elif len(lineup_set) != 9:
            st.error('No duplicates allowed')
        else:
            df = read_team_data(data)
        
            max = 15
            iterations = 1
            original = lineup[:]

            its = st.empty()
            loading_bar = st.progress(0)

            while iterations <= max:
                prog = iterations / 15
        
                its.text(f'Loading {prog*100:.2f}%')
                loading_bar.progress(prog)
            
                lineup, runs = do_flip_optimization(df, original)
                if lineup == original:
                    prog = 1.0
                    loading_bar.progress(prog)
                    its.text('100%')
                    break
                else: 
                    original = lineup[:]

                iterations += 1

            col1, col2 = st.columns(2)
            with col1:
                st.write("""## Original Lineup:""")
                st.write(lineup)
            with col2:
                st.write("""## Optimized Lineup:""")
                st.write(lineup)


def main():
    st.set_page_config(
        page_title="NESCAC Baseball Batting Order Optimization",
        page_icon="images/nescac-logo.png"
    )

    st.title("NESCAC Baseball Batting Order Optimization")

    team_list = ['<select>', 'Amherst', 'Bates', 
                'Bowdoin', 'Colby', 'Hamilton', 'Middlebury', 
                'Trinity', 'Tufts', 'Wesleyan', 'Williams']

    your_team = st.selectbox('Select Your Team:', team_list)

    if your_team != '<select>':
        st.write('You selected:', your_team)

        logo_filename = your_team + '-logo.png'
        logo = Image.open('images/' + logo_filename)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('')
        with col2:
            st.image(logo)
        with col3:
            st.write('')


        data_location = st.radio('Would you like to use 2021 Season data or upload a new file?', 
                                 ['2021 Season', 'Upload'])

        valid = False
        if data_location == 'Upload':
            your_team_data = get_new_data()
            if your_team_data is not None:
                valid = check_file(your_team_data)
                if not valid:
                    st.error("try again fool")
        else:
            filename = 'rosters/' + your_team + '_roster.csv'
            your_team_data = pd.read_csv(filename)
            valid = True

        if valid:
            your_team_players = your_team_data.Player
            your_team_players = list(your_team_players)
            your_team_players.insert(0, '<select>')

            run_type = st.radio("Select an option:", 
                                ['Predicted # Of Runs', 
                                    'Lineup Optimization',
                                    'Compare Two Lineups'])

            if run_type == "Compare Two Lineups":
                run_compare_lineups(your_team_players, your_team_data)
                # st.write('compare')
            elif run_type == "Predicted # Of Runs":
                run_predicted_runs(your_team_players, your_team_data, your_team)
                st.write('predict')
            else:
                run_lineup_optimization(your_team_players, your_team_data, your_team)
                st.write('optimize')
                           
                    

if __name__ == "__main__":
    main()

