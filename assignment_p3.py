import networkx as nx 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy 
import scipy.stats as stats 
import json
from network_analysis import Network_Analysis
from adjusted_scores import Adjusted_Scores

'''
General Overview and Interpretation

Calculated a json file in which there is a dictionary of players and their scores with other players
they have played with in which they are statistical significantly different 

given this we create a network x graph of players and their relations to others with weight corresponding to how different
and color corresponding to if they play better or play worse.

this file we take a statistically significant different pair that have played the most rounds together 

We highlight this pair on the graph and show histogram distributions to illustrate the relation of all of these nodes and edges
The graph that compares the player to all is not significant in demonstrating this point but is added for more context. 

comment out the ax.hist line in normal distribution for better readibility 

It should be noted that we assume all scores are normally distributed given their standard deviation and mean in the visualization curves 
and may not be neccesarily completely reflected in the histogram distribution

'''
class p3:
    def __init__(self):
        # load data from scripts
        graph = Network_Analysis()
        adjusted = Adjusted_Scores()
        self.graph = graph.create_graph()
        self.adjusted = adjusted.get_adjusted_scores()
        # load json of player comparisons and the list of scores
        with open('json/all_player_comparisons.json', 'r') as file:
            self.all_comparisons_data = json.load(file)
        # load json of only statisticaly significant pairings, given by t_stat and p_value
        with open('json/significant_comparisons.json', 'r') as file:
            self.significant_comparisons_data = json.load(file)
        
    def find_max_length_significant_pair(self):
        # find the players with the most rounds together that have a statistical difference
        all_comparisons_data = self.all_comparisons_data
        significant_comparisons_data = self.significant_comparisons_data
        max_length = 0
        max_pair = None

        for player, comparisons in all_comparisons_data.items():
            for other_player, scores in comparisons.items():
                # only iterate through all players if it is also in significant comparions
                if other_player in significant_comparisons_data.get(player, {}):
                    length = len(scores)
                    if length > max_length:
                        max_length = length
                        max_pair = (player, other_player)

        return max_pair

        
    def plot_normal_distribution(self, ax, data, color, label):
        mean, std = np.mean(data), np.std(data)
        x_values = np.linspace(min(data), max(data), 100)
        y_values = stats.norm.pdf(x_values, mean, std)
        # dotted line for mean
        ax.axvline(mean, color=color, linestyle='dashed', linewidth=1)
        # plotted normal distribution for given values
        ax.plot(x_values, y_values, color=color, linewidth=2, label=label)
        # plotted histogram 
        ax.hist(data, bins='auto', color=color, alpha=0.2,density = True)
  
    def visualize_comparisons(self, max_pair):
        # Set up a figure with a specific grid layout
        fig = plt.figure(figsize=(12, 8))

        # Network graph in the top row
        ax_graph = plt.subplot2grid((2, 2), (0, 0), colspan=2)
        G = self.graph
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_color='grey', node_size=1)
        nx.draw_networkx_edges(G, pos, edge_color='lightgrey')
        nx.draw_networkx_nodes(G, pos, nodelist=[max_pair[0], max_pair[1]], node_color='black', node_size=25)
        highlight_edge_color = G[max_pair[0]][max_pair[1]]['color'] if 'color' in G[max_pair[0]][max_pair[1]] else 'red'
        nx.draw_networkx_edges(G, pos, edgelist=[max_pair], edge_color=highlight_edge_color)
        ax_graph.title.set_text("Network Graph")

        # Preparing the data for the histogram distributions
        all_scores = self.adjusted['adjusted_round_score'].tolist()
        player1_scores = self.adjusted[self.adjusted['player_name'] == max_pair[0]]['adjusted_round_score'].tolist()
        player1_score_with_player2 = self.all_comparisons_data[max_pair[0]][max_pair[1]]

        # First all players compared to player 1 
        ax_dist1 = plt.subplot2grid((2, 2), (1, 0))
        self.plot_normal_distribution(ax_dist1, all_scores, 'gray', 'All Scores')
        self.plot_normal_distribution(ax_dist1, player1_scores, 'blue', f"{max_pair[0]} Scores")
        ax_dist1.set_title(f"Distribution of All Adjusted Scores vs. {max_pair[0]}")
        ax_dist1.set_xlabel('Score')
        ax_dist1.set_ylabel('Density')
        ax_dist1.legend()

        # Second player 1 vs player 1 when playing with player 2
        ax_dist2 = plt.subplot2grid((2, 2), (1, 1))
        self.plot_normal_distribution(ax_dist2, player1_score_with_player2, 'red', f" Scores of {max_pair[0]} with {max_pair[1]}")
        self.plot_normal_distribution(ax_dist2, player1_scores, 'blue', f"Scores of {max_pair[0]}")
        ax_dist2.set_title(f"Normal Distribution of Scores for {max_pair[0]} ")
        ax_dist2.set_xlabel('Score')
        ax_dist2.set_ylabel('Density')
        ax_dist2.legend()

        # show all plots
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    data = p3()
    max_pair = data.find_max_length_significant_pair()
    data.visualize_comparisons(max_pair)
 