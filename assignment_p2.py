import pandas as pd    
import matplotlib.pyplot as plt
from scipy.stats import linregress
import glob 
import os 



'''
Broad Overview
One of golf's statistics is shots gained, This statistic identifies performance from various categories to determine 
how many shots in the round they 'shaved' off

The data is for every player for every round and every tournament in the past 4 years. 

the total of all these categories add up to sg_total. Through this analysis I aim to compare which of these 
subcategories predicts a greater sg_total

Since Sg_total is cumultive all of these linear regresiion models will be positive, however the steeper line
will be a better predictor. 



'''
class p2: 
    def __init__(self):
        # Find file from raw_data folder, initialize data frame
        path_to_data ='raw_data'
        self.table = pd.DataFrame()
        # add the contents of each file/season to the bottom of the data fram
        for file in glob.glob(os.path.join(path_to_data, '*.csv')):
            if file.__contains__('raw_data_'):
                print(file)
                season = pd.read_csv(file)
                self.table = pd.concat([self.table,season],ignore_index=True)

        # drop any NA values in any of these collums 
        self.table = self.table.dropna(subset = ['sg_total','sg_putt','sg_arg','sg_app','sg_ott'])

    def get_stats(self):
        # Create lists of the different stats we want to compare 
        self.sg_total = self.table['sg_total'].tolist()

        # sub categories which will be summed with a couple other categories to get sg_total
        self.sg_putt = self.table['sg_putt'].tolist()
        self.around_the_green = self.table['sg_arg'].tolist()
        self.approach = self.table['sg_app'].tolist()
        self.off_the_tee = self.table['sg_ott'].tolist()
       

    def graph(self):
        # create scatter plots for all of the variables to total shots gained 
        # as well as creating corresponding linear regressions for the plots
        y = self.sg_total
        fig, axs = plt.subplots(3, 2, figsize=(12,18))

        # sg_putt vs sg_total
        slope, intercept, _, _, _ = linregress(self.sg_putt, y)
        axs[0,0].scatter(self.sg_putt, y, color='blue', label='SG Putt')
        axs[0,0].plot(self.sg_putt, [slope*x + intercept for x in self.sg_putt], 'k')
        axs[0,0].set_xlabel("SG Putt")
        axs[0,0].set_xlabel("SG Putt")
        axs[0,0].set_ylabel("SG Total")
        axs[0,0].legend()

        # around the green vs sg_total
        slope, intercept, _, _, _ = linregress(self.around_the_green, y)
        axs[0,1].scatter(self.around_the_green, y, color='red', label='Driving Distance')
        axs[0,1].plot(self.around_the_green, [slope*x + intercept for x in self.around_the_green], 'k')
        axs[0,1].set_xlabel("Driving Distance")
        axs[0,1].set_ylabel("SG Total")
        axs[0,1].legend()

        # approach vs sg_total
        slope, intercept, _, _, _ = linregress(self.approach, y)
        axs[1,0].scatter(self.approach, y, color='green', label='Approach')
        axs[1,0].plot(self.approach, [slope*x + intercept for x in self.approach], 'k')
        axs[1,0].set_xlabel("Approach")
        axs[1,0].set_ylabel("SG Total")
        axs[1,0].legend()

        # off the tee vs. sg_total
        slope, intercept, _, _, _ = linregress(self.off_the_tee, y)
        axs[1,1].scatter(self.off_the_tee, y, color='magenta', label='Off the Tee')
        axs[1,1].plot(self.off_the_tee, [slope*x + intercept for x in self.off_the_tee], 'k')
        axs[1,1].set_xlabel("Off the Tee")
        axs[1,1].set_ylabel("SG Total")
        axs[1,1].legend()

        # Compare linear regression of all stats 
        slope, intercept, _, _, _ = linregress(self.sg_putt, y)
        axs[2, 0].plot(self.sg_putt, [slope*x + intercept for x in self.sg_putt], 'b', label='SG Putt Regression')
        slope, intercept, _, _, _ = linregress(self.around_the_green, y)
        axs[2, 0].plot(self.around_the_green, [slope*x + intercept for x in self.around_the_green], 'r', label='Around the Green Regression')
        slope, intercept, _, _, _ = linregress(self.approach, y)
        axs[2, 0].plot(self.approach, [slope*x + intercept for x in self.approach], 'g', label='Approach Regression')
        slope, intercept, _, _, _ = linregress(self.off_the_tee, y)
        axs[2, 0].plot(self.off_the_tee, [slope*x + intercept for x in self.off_the_tee], 'm', label='Off the Tee Regression')
        axs[2, 0].legend()

        plt.show()

if __name__ == '__main__':
    p = p2()
    p.get_stats()
    p.graph()


