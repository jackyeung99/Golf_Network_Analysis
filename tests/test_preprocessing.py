import pytest 
import pandas as pd
import difflib
import sys
sys.path.append('../')
from performance_analytics_project.preprocessing import PreProcessing as pp


class Test_preprocessing:
    def setup_method(self):
        processed = pp()
        self.tourn_data  = processed.process_adjustment()
        self.main_data = processed.process_raw_scores()
        self.merge = processed.merge()

    def test_events(self):
        # premerged data 
        grouped = self.tourn_data.groupby('season')['event_name'].unique().to_list()
        grouped_from_raw = self.main_data.groupby('season')['event_name'].unique().to_list()
        
        difference = len(grouped_from_raw) - len(grouped)
        overlap = len(grouped_from_raw) + difference

        # merged data 
        grouped_merged = self.merge.groupby('season')['event_name'].unique().to_list()

        
        assert len(grouped_merged) == overlap

    def test_scores(self):
        # Filter for one player at one event 
        df = self.tourn_data
        df_rounds = self.main_data
        filtered_row = df[
                        (df['season'] == '2021-2022') & 
                        (df['event_name'] == 'U.S. Open') & 
                        (df['player_name'] == 'Homa, Max')
                        ]
        score_value = filtered_row['total_strokes'].iloc[0]
    
        filtered_total = df_rounds[
                        (df_rounds['season'] == '2021-2022') & 
                        (df_rounds['event_name'] == 'U.S. Open') & 
                        (df_rounds['player_name'] == 'Homa, Max')
                        ]

        tourn_rounds = filtered_total['round_score'].sum()
    
        assert score_value == tourn_rounds
       
    def test_more_scores(self): 

        df = self.merge

        expected = 70 

        actual = df[(df['player_name'] == 'Clark, Wyndham') 
                    & (df['event_name'] == 'U.S. Open')
                    & (df['season'] == '2022-2023')
                    & (df['round_num'] == 4)]
       
        actual = actual['round_score'].iloc[0]

        assert expected == actual

    def test_adjustment(self): 

        df = self.merge

        expected = -7.038

        actual = df[(df['player_name'] == 'Clark, Wyndham') 
                    & (df['event_name'] == 'U.S. Open')
                    & (df['season'] == '2022-2023')
                    & (df['round_num'] == 4)]

        actual = actual['total_adjustment'].iloc[0]

        assert expected == actual