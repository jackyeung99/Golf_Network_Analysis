from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd 
import time
import csv



class Golf_scraper(): 

    def __init__(self):
        self.data = pd.DataFrame()


    def setup(self):
        opts = webdriver.ChromeOptions()
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-gpu')
        # opts.add_argument('--headless')
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options = opts)

    def hover_and_click(self,element):
        action = ActionChains(self.driver)
        if isinstance(element, tuple):
            # If 'element' is a tuple containing use (By, locator) it to locate the element
            by, locator = element
            elem = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((by, locator)))
        else:
            elem = element 

        # hover over the element and click on it
        action.move_to_element(elem).perform()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(elem))
        elem.click()

    def get_table_data(self,year_text,tournament_text):
        # Create pandas table from the html table
        table_element = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div/div/main/div/div[7]/div[2]/div/div/div/div[1]/div[2]/div/div/div/table')
        table = table_element.get_attribute('outerHTML')
        tables = pd.read_html(table)
        # pd.read_html returns a list of tables, find first and only for this website
        table = tables[0]
        # create collumns for the season and tournament 
        table.insert(0,'Season year',[year_text for _ in range(len(table.index))]) 
        table.insert(1,'Tournament',[tournament_text for _ in range(len(table.index))])
        # add table to the bottom
        self.data = pd.concat([self.data, table], ignore_index=True)

    def find_drop_down_menu(self,drop):
        # locate the drop down by index of a list of drop downs in the header
        if 0 <= drop <= 3:
            drop_down_lists = self.driver.find_elements(By.CLASS_NAME, 'css-mcc4c4')
            season_menu = drop_down_lists[drop].find_elements(By.TAG_NAME, 'button')
            return season_menu
        else:
            raise ValueError('wrong index of drop down, there are 3 options')

    def find_stats(self,years_to_scrape):
        self.driver.get('https://www.pgatour.com/stats/detail/120')

        '''
        for each dropdown need to first click on the drop down 
        then find the element in the drop down
        then click on that element
        '''

        # Set time period to tournament only 
        self.hover_and_click((By. XPATH, "//button[contains(.,'Time Period')]" ))
        time_frame_menu = self.find_drop_down_menu(1)
        self.hover_and_click(time_frame_menu[1])
        time.sleep(3)

        for season in range(years_to_scrape):
            # iteratate through seasons 
            self.hover_and_click((By.XPATH, '//span[contains(., "Season")]'))
            season_menu = self.find_drop_down_menu(0)
            season_text = season_menu[season].text
            print(season_text)
            self.hover_and_click(season_menu[season])   
            time.sleep(3)
          
            for idx in range(len(self.find_drop_down_menu(2))):
                # iterate through each tournament 
                self.hover_and_click((By.XPATH,"//button[contains(.,'Tournament')][not(contains(.,'Tournament Only'))]"))
                tournament_menu = self.find_drop_down_menu(2)
                tournament_text = tournament_menu[idx].text
                print(tournament_text)
                self.hover_and_click(tournament_menu[idx])
                
                time.sleep(3)
                # Scrape data 
                self.get_table_data(season_text,tournament_text)     

    def dump(self):
       
       self.data.to_csv('raw_data\tournament_data.csv')
    
if __name__ == '__main__':
    scraper = Golf_scraper()
    data = scraper.__init__()
    scraper.setup()
    scraper.find_stats(4)
    scraper.dump()


# with pd.option_context('display.max_rows', 20, 'display.max_columns', None): print(data)
