from asyncio import run
import streamlit as st
import csv
import pandas as pd
from PIL import Image
#import re, math
import random
from itertools import permutations
import time

def read_team_data(filename):
    team_data = pd.read_csv(filename)
    df = pd.DataFrame(team_data)

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
        
        # thresholds[df['Player'][i]] = []

        
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

    # st.write(thresholds)
    return thresholds


def run_monte_carlo(thresholds):
    #start = time.perf_counter()
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

    #end = time.perf_counter()
    #st.write(end - start)
    return game_state['Runs']

def avg_runs(thresholds):
    start_time = time.perf_counter()
    runs = []
    for i in range(1000):
        runs.append(run_monte_carlo(thresholds))

    end_time = time.perf_counter()
    st.write(end_time - start_time)
    return (sum(runs) / len(runs))

def optimize_lineup(df, players):
    # st.write("Permutations: ")
    # st.write(list(permutations(players)))

    perms = list(permutations(players))
    curr_max = 0
    curr_best_lineup = []
    start_time = time.perf_counter()

    for perm in perms:
        thresholds = calculate_thresholds(df, perm)
        avg = run_monte_carlo(thresholds)

        # for i in range(1000):
        #     runs.append(run_monte_carlo(thresholds))
        # avg = (sum(runs) / len(runs))

        # st.write(avg)
        # st.write(perm)
        # st.write('-------')
        if avg > curr_max:
            curr_max = avg
            curr_best_lineup = perm

    st.write("Best: ")
    st.write(curr_max)
    st.write(curr_best_lineup)
    end_time = time.perf_counter()
    st.write(end_time - start_time)

    

st.write("""
         ## Monte Carlo Simulations for Batting Order Optimization (Change Me Later)
         """)

team_list = ['No Selection', 'Amherst', 'Bates', 
             'Bowdoin', 'Colby', 'Hamilton', 'Middlebury', 
             'Trinity', 'Tufts', 'Wesleyan', 'Williams']

# col1, col2 = st.columns(2)
# with col1:
your_team = st.selectbox('Select Your Team:', team_list)

if your_team != 'No Selection':
    st.write('You selected:', your_team)
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

# with col2:
#     opponent = st.selectbox('Select Your Opponent:', team_list)

#     if opponent != 'No Selection':
#         st.write('You selected:', opponent)
#         logo_filename2 = opponent + '-logo.png'
#         logo2 = Image.open('images/' + logo_filename2)
#         cap2 = opponent + ' Logo'
#         st.image(logo2)
        

if your_team != 'No Selection':

    # get the your_team name and read in the data from the csv for that your_team
    filename = 'rosters/' + your_team + '_roster.csv'

    
    your_team_data = pd.read_csv(filename)
    your_team_players = your_team_data.Player

    run_type = st.radio("Select an option:", ['# Of Runs', 'Lineup Optimization'])

    message1 = 'Select the players for the ' + your_team + ' lineup:'
    your_team_selected = st.multiselect(message1, your_team_players)

    #st.write(your_team_selected)

    if st.button('Submit'):
        df = read_team_data(filename)
    
        if run_type == '# Of Runs':
            thresholds = calculate_thresholds(df, your_team_selected)
            st.title("Number of predicted runs: " + str(avg_runs(thresholds)))
        else:
            st.title('Fuck Alex')
            optimize_lineup(df, your_team_selected)


# if opponent != 'No Selection':

#     # get the your_team name and read in the data from the csv for that your_team
#     filename2 = opponent + '_roster.csv'

#     opponent_data = pd.read_csv('rosters/' + filename2)
#     opponent_players = opponent_data.Player

#     message2 = 'OPTIONAL: Sel' + opponent + ' lineup:'
#     opponent_selected = st.multiselect(message2, opponent_players)

#     st.write(opponent_selected)

