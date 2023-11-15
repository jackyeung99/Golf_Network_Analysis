import pytest 
import pandas as pd
import difflib
import sys
sys.path.append('../')
from performance_analytics_project.adjusted_scores import Adjusted_Scores as AS


class Test_Basics:

    @pytest.fixture 
    def basics(self):
        Adjusted = AS()
        main_data = Adjusted.get_adjusted_scores()
        tournament_avg = Adjusted.tournament_adjustments()
        return main_data,tournament_avg

    def test_average(self,basics):
       
        _, tournament_avg = basics
        df = tournament_avg
        
        actual = df[(df['event_name'] == 'U.S. Open')
                    & (df['season'] == '2022-2023')]

        actual = (actual['total_adjustment'].iloc[0])
         # actual is -7.038 without rounding
        expected = -7.04
       

        assert actual == expected

    def test_num_events(self,basics):
        _ , tournament_avg = basics
        df = tournament_avg
        
        expected_tournaments = 150 
        num_actual_tournament = len(df)

        assert expected_tournaments == num_actual_tournament

    def test_missed_cut(self,basics):
        main_data, _ = basics 

        df = main_data
        actual = df[(df['event_name'] == 'U.S. Open')
                    & (df['season'] == '2022-2023')
                    & (df['player_name'] == 'Im, Sungjae')
                    & (df['round_num'] == 2)
                    ]
        
        actual_round = actual['round_adjustment'].iloc[0]
       
        expected_round = -1.76


        assert actual_round == expected_round

    def test_missed_adjusted(self,basics):
        main_data, _ = basics 

        df = main_data
        actual = df[(df['event_name'] == 'U.S. Open')
                    & (df['season'] == '2022-2023')
                    & (df['player_name'] == 'Im, Sungjae')
                    & (df['round_num'] == 2)
                    ]
        
        actual_adjusted = actual['adjusted_round_score'].iloc[0]
       
        expected_adjusted = -1.76 + 75


        assert actual_adjusted == expected_adjusted

    def test_made_cut(self,basics):
        main_data, _ = basics 

        df = main_data
        actual = df[(df['event_name'] == 'U.S. Open')
                    & (df['season'] == '2022-2023')
                    & (df['player_name'] == 'Clark, Wyndham')
                    & (df['round_num'] == 4)
                    ]
        
        actual_round = actual['adjusted_round_score'].iloc[0]
       
        expected_round = -1.76 + 70


        assert actual_round == expected_round

    def test_different_adjustment_stats(self,basics):
        _, tournament_avg = basics 

        df = tournament_avg
        actual = df[(df['event_name'] == 'AT&T Pebble Beach Pro-Am')
                    & (df['season'] == '2019-2020')
                    ]
        
        actual = (actual['total_adjustment'].iloc[0])
        upper_bound = -.3
        lower_bound = -2.793

        assert lower_bound < actual < upper_bound