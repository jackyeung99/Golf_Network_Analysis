import pandas as pd
from collections import defaultdict
from scipy.stats import ttest_1samp
import numpy as np
import json
from adjusted_scores import Adjusted_Scores

class Player_Comparisons:
    def __init__(self):
        expected = Adjusted_Scores()
        # get adjusted data
        self.main_data = expected.get_adjusted_scores()
        self.player_stats = expected.get_player_avg()

    def analysis(self, round_threshold = 3): 
        # create an empty dictionary with imbedded dictionaries 
        player_combinations = defaultdict(lambda: defaultdict(list))
        table = self.main_data
        # find players who played together
        grouped = table.groupby(['season', 'event_name', 'round_num','course_name','start_hole', 'teetime'])

        for _,group_data in grouped:
            players = group_data['player_name'].to_list()
            scores = group_data['adjusted_round_score'].to_list()
            score_dict = dict(zip(players,scores))

            for player in players:
                # add the score of the main player to the dictionary of the player he was with. 
                player_score = score_dict[player]
                # iterate over other players in group
                other_players = set(players) - set([player])
    
                for other in other_players:
                    # Append the score
                    player_combinations[player][other].append(player_score)

        # given a threshold of scores only take these values
        filtered_combinations = {player: {other: scores for other, scores in comb.items() if len(scores) >= round_threshold} 
                                for player, comb in player_combinations.items()}
        
        return filtered_combinations

    def t_test(self,p_threshold = .05):
        final_combinations = self.analysis()
        significant_results = defaultdict(dict)
        player_means = self.player_stats.set_index('player_name')['mean'].to_dict()
        # perform t-test for each combination
        for player, comp in final_combinations.items():
            player_mean = player_means.get(player)
            for other, scores in comp.items():
                # issue with scores having 0 std and causing inf t-stat values
                if np.std(scores) != 0:
                    # perform t-test
                    t_stat, p_val = ttest_1samp(scores,player_mean)
                    if p_val <= p_threshold:
                        diff = player_mean - np.mean(scores)
                        # append significant results 
                        significant_results[player][other] = {
                            "diff": diff.round(3),
                            "t_stat": t_stat.round(3),
                            "p_val": p_val.round(3)
                        }
          

        return significant_results
    
    def dump(self,data,file):  
        with open(file,'w') as f:
            json.dump(data,f)

    def main(self):
        data = self.analysis()
        self.dump(data,'json/all_player_comparisons.json')
        data2 = self.t_test()
        self.dump(data2,'json/significant_comparisons.json')
   
if __name__ == '__main__':
    analysis = Player_Comparisons()
    analysis.main()