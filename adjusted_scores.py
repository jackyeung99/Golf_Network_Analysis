import pandas as pd 
import glob 
import os
from preprocessing import PreProcessing as pp
import matplotlib.pyplot as plt

'''
In a golf tournament there are a total of 4 rounds, after 2 rounds only the better half 
of players continue to the weekend 

total adjustment is the adjustment to the sum of all rounds 

the data only has total_adjustment for players who made the cut. 
'''

class Adjusted_Scores:
    def __init__(self):
      # get data from preprocessing 
      data = pp()
      self.main_data = data.merge()
      self.avg_data = data.process_adjustment()
      self.average_adjustment = self.tournament_adjustments() 

    def tournament_adjustments(self):
      # sort aquire columns needed 
      df = self.main_data
      df = df[['season', 'event_name', 'total_adjustment']]
      df = df.loc[df['total_adjustment' ].notna()]
      
      # find the mean of adjustments for each tournament
      average_adjustment = df.groupby(['season', 'event_name'])['total_adjustment'].mean().round(2).reset_index()
      average_adjustment['round_adjustment'] = (average_adjustment['total_adjustment'] / 4).round(2)
      return average_adjustment
      
    
    def get_round_adjustments(self):
      # Create copy of data 
      data = self.main_data.copy()  
      # apply average round score to all 
      data = data.merge(self.average_adjustment[['season', 'event_name','round_adjustment']],\
                                                 on=['season', 'event_name'], how='left')
      # if player has total round adjustment calculate it normally 
      num_rounds = 4
      data.loc[data['total_adjustment'].notna(), 'round_adjustment'] = (data['total_adjustment'] / num_rounds).round(2)
      return data 
    
    def get_adjusted_scores(self):
      # use previoulsy calculated round adjustment and apply to gross score to get net score 
      data = self.get_round_adjustments()
      data.loc[:,'adjusted_round_score'] = data['round_score'] + data['round_adjustment']
      return data 

    def get_player_avg(self):
      filter = self.get_adjusted_scores()

      # find various statistics from columns 
      yearly_stats = filter.groupby(['player_name']).agg(
        mean=('adjusted_round_score', 'mean'),
        st_dev=('adjusted_round_score', 'std'),
        sum_strokes = ('round_score', 'sum'),
        total_rds = ('round_score', 'count')
        ).reset_index()
    
      return yearly_stats
  


if __name__ == '__main__':
    expected = Adjusted_Scores()
    data = expected.get_adjusted_scores() 
    data2 = expected.get_player_avg()
    
    
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None): print(data2)
 

