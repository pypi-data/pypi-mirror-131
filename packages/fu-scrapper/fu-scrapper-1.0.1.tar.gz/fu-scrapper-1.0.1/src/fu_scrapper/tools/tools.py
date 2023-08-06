import datetime
import os
from time import sleep

import pandas as pd

from ..tools.Scrapper import Scrapper


class Tools():
    def __init__(self):
        self.data_url = os.path.dirname(os.path.abspath(__file__)) + '/data/'
        self.scrapper = Scrapper(max_call_errors=6)
        
    def get_data(self, url, datasets_name):
        json = self.scrapper.retrieve_json_api_from_url(url=url)

        if json == None:
            return None

        dfs = {}
        for elem in json['resultSets']:
            if elem['name'] not in datasets_name:
                continue

            df = pd.DataFrame(elem['rowSet'], columns=elem['headers'])
            dfs[elem['name']] = df

        return dfs
    
    def get_date(self, days: int, variation="-"):
        if variation == "-":
            date = datetime.date.today() - datetime.timedelta(days=days)
        elif variation == "+":
            date = datetime.date.today() + datetime.timedelta(days=days)
        else:
            print("")
            
        return date.strftime('%Y-%m-%d')
    
    def merge_news_old(self, new_df, old_df):
        return pd.concat([new_df, old_df], sort=False).drop_duplicates().reset_index(drop=True)
    
    def check_dataset(self):
        datasets = ['games.csv','games_details.csv']
        games = pd.read_csv(self.data_url + 'games.csv')

        print('====== GAMES ======')
        print(games.shape)
        print('Min date : %s'%(games['GAME_DATE_EST'].min()))
        print('Max date : %s'%(games['GAME_DATE_EST'].max()))

        games_details = pd.read_csv(self.data_url + 'games_details.csv')
        print('====== GAMES DETAILS ======')
        print(games_details.shape)
        print('N uniques games ID : %i'%(games_details['GAME_ID'].nunique()))
