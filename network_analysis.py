import networkx as nx
import json 


class Network_Analysis:
    def __init__(self):
        # load significant results
        with open('json/significant_comparisons.json','r') as file:
            self.significant_results = json.load(file)
       
    def create_graph(self):
        G = nx.DiGraph()
        # create directed graph from significant player combinations
        for player, others in self.significant_results.items():
            for other_player, stats in others.items():
                # weight is according to total t_stat or the differences in mean
                player_diff = stats['diff']
                # negative values correlate with shooting lower score hence green else red 
                attr = 'green' if player_diff < 0 else 'red'
                G.add_edge(player, other_player, weight=abs(player_diff), color=attr)
        return G

    def main(self):
        G = self.create_graph()
        # write graphml 
   
        nx.write_graphml(G, 'Gephi_graphs/Golf_Network_Graph_3.graphml', named_key_ids=True)

if __name__ == "__main__":
    analysis = Network_Analysis()
    analysis.main()