from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from tournament_scraper import Golf_scraper
import pandas as pd

import time
import csv


class AVG_score_scraper(): 

    def __init__(self):
        self.data = pd.DataFrame()
        self.golf_scraper = Golf_scraper()
        
    def setup(self):
        self.golf_scraper.setup()

    def get_table_data(self,year_text):
        # Create pandas table from the html table
        table_element = self.golf_scraper.driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div/div/main/div/div[7]/div[2]/div/div/div/div[1]/div[2]/div/div/div/table')
        table = table_element.get_attribute('outerHTML')
        tables = pd.read_html(table)
        # pd.read_html returns a list of tables, find first and only for this website
        table = tables[0]
        # create collumns for the season and tournament 
        table.insert(0,'Season year',[year_text for _ in range(len(table.index))]) 
        # add table to the bottom
        self.data = pd.concat([self.data, table], ignore_index=True)


    def get_stats(self,years_to_scrape):
        self.golf_scraper.driver.get('https://www.pgatour.com/stats/detail/120')
        time.sleep(3)
        for season in range(years_to_scrape):
            # iteratate through seasons 
            self.golf_scraper.hover_and_click((By.XPATH, '//span[contains(., "Season")]'))
            season_menu = self.golf_scraper.find_drop_down_menu(0)
            season_text = season_menu[season].text
            print(season_text)
            self.golf_scraper.hover_and_click(season_menu[season])   
            time.sleep(3)
            self.get_table_data(season_text)
            time.sleep(1)
    
    def dump(self):
        self.data.to_csv('raw_data\average_scores.csv')


if __name__ == '__main__':
    scraper = AVG_score_scraper()
    scraper.setup()
    scraper.get_stats(4)
    scraper.dump()