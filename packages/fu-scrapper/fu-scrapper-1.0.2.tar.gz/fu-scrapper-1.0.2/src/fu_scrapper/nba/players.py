import os
from time import time

import pandas as pd
from tools.tools import Tools


class Players():
    def __init__(self, url):
        self.tools = Tools(url)
        self.data_url = url

    def export_players(self):
        """
            Export players informations and global stats
        """
        try:
            # Initialize the timer
            t0 = time()
            # Url of the all players detailes per seasons
            url = 'https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight='

            players = self.tools.get_data(url, datasets_name=['LeagueDashPlayerStats'])
            players = players['LeagueDashPlayerStats']
            players_clean = self.__get_player_info(players)
                        
            if players is not None:
                players_clean.to_csv(self.data_url + 'players.csv')
                
            print('All Players export execution time : %.2fs'%(time()-t0))
            
        except Exception as e:
            raise e
    
    def __get_player_info(self, player_dataset):
        """
            Get all players personnal informations and merge it to current detail dataset
        """
        try:
            # Url to get Teams infos 
            url = 'https://stats.nba.com/stats/leaguedashplayerbiostats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='
            players_details = self.tools.get_data(url, datasets_name=['LeagueDashPlayerBioStats'])
            players_details = players_details['LeagueDashPlayerBioStats']
            
            extract_fields = ['PLAYER_HEIGHT', 'PLAYER_HEIGHT_INCHES', 'PLAYER_WEIGHT', 'COLLEGE', 'COUNTRY', 'DRAFT_YEAR', 'DRAFT_ROUND', 'DRAFT_NUMBER', 'NET_RATING']
            
            for field in extract_fields:
                player_dataset[field] = player_dataset.merge(players_details, on="PLAYER_ID")[field]

            # return updated dataset
            return player_dataset
        except Exception as e:
            raise e
    

# NBA Url for players stats per season
# https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight=


# NBA Url for Players Bios
# https://stats.nba.com/stats/leaguedashplayerbiostats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight=


# NBA Url for Player scoreBoard per season
# https://stats.nba.com/stats/leaguegamelog?Counter=1000&DateFrom=&DateTo=&Direction=DESC&LeagueID=00&PlayerOrTeam=P&Season=2021-22&SeasonType=Regular+Season&Sorter=DATE
