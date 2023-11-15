import pandas as pd    
import glob 
import os 

class PreProcessing:
    def __init__(self):
        self.path_to_data ='raw_data'
        self.get_files()
    
    def get_files(self):
        all_files = glob.glob(os.path.join(self.path_to_data, 'raw_data_*.csv'))
        data_frames = [pd.read_csv(file) for file in all_files]
        self.total_table = pd.concat(data_frames, ignore_index=True)
        self.total_table = self.total_table[['season', 'event_name', 'player_name', 'fin_text', 'round_num','course_name','start_hole', 'teetime', 'round_score']]

    def rearrange_name(self,name):
            name = name.strip()
            parts = name.split(' ')
            if len(parts) > 1:
                # Format for three parts: "Last Middle, First"
                return ' '.join(parts[1:])  + ', ' + parts[0]
            else:
                # If the name format doesn't match expectations, return it unchanged or handle it as needed
                return name
            
    def process_adjustment(self):
        path = 'raw_data\\tournament_data.csv'
        raw_table = pd.read_csv(path)
        raw_table = raw_table.map(lambda x: x.strip() if isinstance(x, str) else x)
        raw_table.columns = [col.strip() for col in raw_table.columns]
        raw_table.rename(columns = {
            'Season year' :'season',
            'Tournament':'event_name',
            'Rank':'fin_text',
            'Player':'player_name',
            'Avg':'avg',
            'Total Strokes':'total_strokes',
            'Total':'total',
            'Total Adjustment':'total_adjustment',
            'Total Rounds':'total_Rounds'
              },inplace = True)
    
        # Drop duplicates,rows with field average, NA rows, and unamed columns 
        raw_table = raw_table[(raw_table['player_name'] != 'field average') & (raw_table['player_name'].notna())].drop_duplicates()
        columns_to_keep = [column for column in raw_table.columns if not column.lower().startswith('unnamed')]
        raw_table = raw_table[columns_to_keep]
      
        raw_table = raw_table[~raw_table['event_name'].str.startswith('Fortinet')]

        # convert name to same format as main data 
        raw_table['player_name'] = raw_table['player_name'].apply(self.rearrange_name)
        # convert adjustment to a numeric and remove spaces
        raw_table['total_adjustment'] = pd.to_numeric(raw_table['total_adjustment'].replace(r'[^\d.-]', '', regex=True), errors='coerce')

        # for season with the same tournament twice, change the first one to a year back 
        year_change_needed = ['U.S. Open (2020)', 'Corales Puntacana Resort & Club Championship (2020)','Masters Tournament (2020)']
        for tournament in year_change_needed:
            mask = (raw_table['event_name'] == tournament) & (raw_table['season'] == '2020-2021')
            raw_table.loc[mask, 'season']  = '2019-2020'
            
       
        # remove year parenthesis to keep consitancy
        replacements = {
            # 2019-2020
            'Corales Puntacana Resort & Club Championship (2020)': 'Corales Puntacana Resort & Club Championship',
            'U.S. Open (2020)':'U.S. Open',
            'Masters Tournament (2020)':'Masters Tournament',
            # 2020-221
            'Corales Puntacana Resort & Club Championship (2021)': 'Corales Puntacana Resort & Club Championship',
            'U.S. Open (2021)':'U.S. Open',
            'Masters Tournament (2021)':'Masters Tournament',
            # 2022-2023
            'World Wide Technology Championship' : 'World Wide Technology Championship at Mayakoba'
                    }
        raw_table.loc['event_name'] = raw_table['event_name'].replace(replacements)

        processed_table = raw_table.reset_index()
        return processed_table
    
    
    def process_raw_scores(self):
        # General preparation for merge
        total_table = self.total_table.copy()
        unfiltered_total_table = total_table[~total_table['event_name'].str.startswith('Fortinet')].copy()
        
        # Modify the 'season' column
        unfiltered_total_table.loc[:, 'season'] = unfiltered_total_table['season'].apply(lambda x: str(int(x) - 1) + '-' + str(x))
        # random name error
        unfiltered_total_table.loc[:, 'player_name'] = unfiltered_total_table['player_name'].str.replace('van Tonder, Danie', 'van Tonder, Daniel')

        year_change_needed = ['U.S. Open', 'Corales Puntacana Resort & Club Championship','The Masters']
        for tournament in year_change_needed:
            mask = (unfiltered_total_table['event_name'] == tournament) & (unfiltered_total_table['season'] == '2020-2021')
            unfiltered_total_table.loc[mask, 'season'] = '2019-2020'

        unfiltered_total_table.loc[:, 'event_name'] = unfiltered_total_table['event_name'].str.replace(' #2', '')

        # replace masters to masters tournament 
        replace = {'The Masters':'Masters Tournament'}
        unfiltered_total_table.loc[:, 'event_name'] = unfiltered_total_table['event_name'].replace(replace)

        cleaned_total_table = unfiltered_total_table.reset_index()
        return cleaned_total_table 

    def merge(self):
        tournament_adjusted = self.process_adjustment()
        total_table = self.process_raw_scores()
        # Identify common tournaments
        common_tournaments = pd.merge(total_table[['event_name', 'season']].drop_duplicates(), 
                                    tournament_adjusted[['event_name', 'season']].drop_duplicates(), 
                                    on=['event_name', 'season'])

        # Filter the round scores dataframe to only include common tournaments
        df_round_scores = total_table.merge(common_tournaments, on=['event_name', 'season'])

        # Now, merge on the common keys (tournaments and players)
        merged_df = df_round_scores.merge(tournament_adjusted[['event_name', 'season', 'player_name','total_adjustment']], 
                                        on=['event_name', 'season', 'player_name'], 
                                        how='left')       
        final_merged = merged_df.reset_index(drop=True)
        return final_merged
    
    def main(self):
        df = self.merge()
        # d2 = self.process_raw_scores()
        print(len(df[['event_name','season']].drop_duplicates()))
        # print(len(d2[['event_name','season']].drop_duplicates()))
   
        with pd.option_context('display.max_rows', 100, 'display.max_columns', None): print(df)
    

if __name__ == '__main__':
   analysis = PreProcessing()
   analysis.main()