import pytest 
import pandas as pd
import difflib
import sys
sys.path.append('../')
from performance_analytics_project.player_rating import Player_Comparisons as PC
from performance_analytics_project.adjusted_scores import Adjusted_Scores as AS


class Test_Basics:
    @pytest.fixture
    def basics(self):
        comparisons = PC()
        all_comparisons = comparisons.analysis()
        significant = comparisons.t_test()
        return all_comparisons,significant
    
    @pytest.fixture
    def adjusted_basics(self):
        adjusted = AS()
        main_avg = adjusted.get_player_avg()
        return main_avg

    def test_size(self,adjusted_basics):
        comp = PC()
        threshold = 0
        all_comparisons = comp.analysis(threshold)
        
        average_scores = adjusted_basics

        assert len(all_comparisons.keys()) == len(average_scores)

    # def test_self(self,basics):
    #     comparisons, _ = basics
    #     for player in comparisons:
    #         assert player[player] not in comparisons


if __name__ == "__main":
    data = Test_Basics
    data.test_size()