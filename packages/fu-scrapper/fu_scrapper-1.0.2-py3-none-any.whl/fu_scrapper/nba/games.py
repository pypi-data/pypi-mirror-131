import datetime
import os
from time import sleep, time

import joblib
import pandas as pd
from tools.preformator import Preformator
from tools.tools import Tools


class Games():
    """
        Games class to get all NBA stats and ranking
    """
    def __init__(self, url):
        self.tools = Tools(url)
        self.data_url = url
        
    def next_week_games(self):
        """
            Get next week games
        """
        try:
            # Initialize the timer
            t0 = time()
            
            for i in range(1,8):
                date = self.tools.get_date(i,"+")
                url = 'https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate='+date
                games = self.tools.get_data(url, datasets_name=['GameHeader'])
                games = games['GameHeader']
                
                if games is not None:
                    games.to_csv(self.data_url + 'daily/games_'+ date +'.csv')
                    
            print('Next week Teams export execution time : %.2fs'%(time()-t0))
        except Exception as e:
            raise e
        
    def last_week_games(self):
        """
            Get last week games
        """
        try:
            # Initialize the timer
            t0 = time()
            
            for i in range(1,8):
                date = self.tools.get_date(i,"-")
                url = 'https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate='+date
                games = self.tools.get_data(url, datasets_name=['GameHeader'])
                games = games['GameHeader']
                
                if games is not None:
                    games.to_csv(self.data_url + 'daily/games_'+ date +'.csv')
                    
            print('Last week games export execution time : %.2fs'%(time()-t0))
        except Exception as e:
            raise e

    def today_games(self):
        """
            Get Today games
        """
        try:
            # Initialize the timer
            t0 = time()
            
            date = datetime.date.today().strftime('%Y-%m-%d')
            url = 'https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate='+date
            games = self.tools.get_data(url, datasets_name=['GameHeader'])
            games = games['GameHeader']
            
            if games is not None:
                games.to_csv(self.data_url + 'daily/games_'+ date +'.csv')
                    
            print('Today games export execution time : %.2fs'%(time()-t0))
        except Exception as e:
            raise e
    
    def new_games(self):
        """
            Get games and ranking data and update old datasets
        """
        t0 = time()
        try:
            # Load old datasets
            old_games = pd.read_csv(self.data_url + 'games.csv')
            old_ranking = pd.read_csv(self.data_url + 'ranking.csv')
            old_games_details = pd.read_csv(self.data_url + 'games_details.csv')
        except Exception as e:
            raise e(
                'games.csv should be in the data/ directory, if you don\'t have the current games.csv.'
            )

        max_date = old_games['GAME_DATE_EST'].max()
        
        if max_date == self.tools.get_date(1):
            print('Last update is yesterday : end script now.')
            return

        print('Last updated date : ', str(max_date))

        # Dataset to retrieve from api
        datasets = [
            'GameHeader', 'LineScore', 'EastConfStandingsByDay',
            'WestConfStandingsByDay'
        ]
        ignore_keys = ['date']

        # init dictionnary to collect data
        dfs = {}
        for dataset in datasets + ignore_keys:
            dfs[dataset] = list()

        # Be sure this file is the save of the current run
        save_path = 'games.sav'
        if os.path.exists(save_path):
            dfs = joblib.load(save_path)
            min_date_already_saved = min(dfs['date'])
        else:
            min_date_already_saved = '2100-01-01'

        # Use a for loop to avoid while(True) infinite loop
        for i in range(1, 10000):
            date = self.tools.get_date(i,"-")

            if date <= max_date:
                break
            elif date >= min_date_already_saved:
                continue

            url = 'https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate=' + date

            game_day_dfs = self.tools.get_data(url=url, datasets_name=datasets)
            game_day_dfs['date'] = date
            sleep(0.2)

            print('There are %i games this day' % len(game_day_dfs['GameHeader']))

            for dataset in game_day_dfs.keys():
                dfs[dataset].append(game_day_dfs[dataset])

            joblib.dump(dfs, save_path)

        # convert to pandas DataFrame
        for dataset in dfs.keys():
            if dataset in ignore_keys:
                continue
            dfs[dataset] = pd.concat(dfs[dataset])
            print(dataset, dfs[dataset].shape)

        header_cols = [
            'GAME_DATE_EST', 'GAME_ID', 'GAME_STATUS_TEXT', 'HOME_TEAM_ID',
            'VISITOR_TEAM_ID', 'SEASON'
        ]
        linescore_cols = [
            'GAME_ID', 'TEAM_ID', 'PTS', 'FG_PCT', 'FT_PCT', 'FG3_PCT', 'AST',
            'REB'
        ]

        # Get wanted datasets with wanted columns
        west_ranking = dfs['WestConfStandingsByDay']
        east_ranking = dfs['EastConfStandingsByDay']
        games_header = dfs['GameHeader'][header_cols]
        line_score = dfs['LineScore'][linescore_cols]

        del dfs

        # Preformat NBA data
        print('Preformat nba data')
        preformater = Preformator(
            games_header, line_score, west_ranking, east_ranking,self.data_url)
        new_games = preformater.preformat_games()
        new_ranking = preformater.preformat_ranking()

        del games_header, line_score, west_ranking, east_ranking

        dfs_details = list()

        # Be sure this file is the save of the current run
        save_details_path = 'games_details.sav'
        game_details_already_saved = []

        if os.path.exists(save_details_path):
            dfs_details = joblib.load(save_details_path)
            game_details_already_saved = pd.concat(dfs_details)['GAME_ID'].unique()

        # Retrieve game detail
        print('Retrieve new games details, # of games to get : ',
            str(len(new_games['GAME_ID'])))
        for game_id in new_games['GAME_ID']:
            if game_id in game_details_already_saved:
                continue

            df = self.__get_game_detail(game_id)
            if len(df) == 0:
                print('No data found')

            dfs_details.append(df)

            joblib.dump(dfs_details, save_details_path)

        new_games_details = pd.concat(dfs_details)

        # Merge old and new dataframe
        print('Merging old and new datasets')
        ranking = self.tools.merge_news_old(new_ranking, old_ranking)
        games = self.tools.merge_news_old(new_games, old_games)
        games_details = self.tools.merge_news_old(new_games_details, old_games_details)

        games['GAME_ID'] = pd.to_numeric(games['GAME_ID'])
        games['GAME_DATE_EST'] = pd.to_datetime(games['GAME_DATE_EST'])
        games_details['GAME_ID'] = pd.to_numeric(games_details['GAME_ID'])
        ranking['STANDINGSDATE'] = pd.to_datetime(ranking['STANDINGSDATE'])

        # Save merge datasets
        print('Save new datasets to csv into ', self.data_url)
        today = self.tools.get_date(0)
        games.to_csv(self.data_url + 'games.csv', index=False)
        games_details.to_csv(self.data_url + 'games_details.csv', index=False)
        ranking.to_csv(self.data_url + 'ranking.csv', index=False)

        print('Delete tmp saved files')
        os.remove(save_path)
        os.remove(save_details_path)
        
    def __get_game_detail(self, game_id):
        """
            Get game details
            TODO :
                Url season setup to get data
        """
        if type(game_id) != type(str()):
            game_id = '00' + str(game_id)

        url = 'https://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=0&GameID='+str(game_id) \
            + '&RangeType=0&Season=2021-22&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'

        df = self.tools.get_data(url, datasets_name=['PlayerStats'])
        sleep(0.2)
        return df['PlayerStats']
