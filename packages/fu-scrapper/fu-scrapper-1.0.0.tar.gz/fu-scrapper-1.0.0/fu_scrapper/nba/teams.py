import os
from time import time

import pandas as pd
from tools.tools import Tools


class Teams():
    """
        Team class to get all NBA teams informations and details
    """
    def __init__(self):
        self.tools = Tools()
        self.data_url = os.path.dirname(os.path.abspath(__file__)) + '/data/'
        
    def export_teams(self):
        """
            Function to export teams into csv file
            TODO :
                Url season setup to get data
        """
        try:
            # Initialize the timer
            t0 = time()
            # Url of the all team detailes per seasons
            url = 'https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision='
            teams = self.tools.get_data(url, datasets_name=['LeagueDashTeamStats'])
            teams = teams['LeagueDashTeamStats']
            teams_clean = self.__get_team_info(teams)
            
            if teams_clean is not None:
                teams_clean.to_csv(self.data_url + 'teams.csv')
                
            print('Export all Teams execution time : %.2fs'%(time()-t0))
            
        except Exception as e:
            raise e
        
    def export_team_detail(self):
        """
            Function to export teams detailes into csv file
            Concat with the teams dataset with the actual team detaile dataset
        """
        try:
            # Initialize the timer
            t0 = time()
            teams = self.__get_team()
            # Extract the season scoreboard per team
            teams_detail = teams['TEAM_ID'].apply(lambda x: self.__get_team_detail(x))
            
            # Concat teams details dataset values
            teams_detail = pd.concat(teams_detail.values)
            
            if teams_detail is not None:
                teams_detail.to_csv(self.data_url + 'teams_details.csv')
                
            print('Export Teams details execution time : %.2fs'%(time()-t0))
            
        except Exception as e:
            # TODO Put a print() to replace the raise
            raise e
        
    def __get_team_detail(self, team_id: int):
        """
            Private function return the Team scoreboard Year by Year 
            Pandas dataFrame with a new columnn TEAM_ID
            TODO :
                Url season setup to get data
        """
        try:
            # Url of the Team scoreboard year by year
            team_detail_url = 'https://stats.nba.com/stats/teamdashboardbyyearoveryear?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlusMinus=N&Rank=N&Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&Split=yoy&TeamID='+ str(team_id) +'&VsConference=&VsDivision='
            df = self.tools.get_data(team_detail_url, datasets_name=['ByYearTeamDashboard'])
            # Add column into current team detail dataset
            df['ByYearTeamDashboard']['TEAM_ID'] = team_id
            # return team detaile dataset with the TEAM_ID column
            return df['ByYearTeamDashboard']
        except Exception as e:
            raise e
    
    def __get_team(self):
        """
            Return Teams infomations
        """
        try:
            # Url of the all team detailes per seasons
            url = 'https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision='
            teams = self.tools.get_data(url, datasets_name=['LeagueDashTeamStats'])
            return teams['LeagueDashTeamStats']
        except Exception as e:
            raise e
    
    def __get_team_info(self, teams_dataset):
        """
            Return Team info dataset
        """
        try:
            # Url to get Teams infos 
            url = 'https://stats.nba.com/stats/commonteamyears?LeagueID=00'
            teams = self.tools.get_data(url, datasets_name=['TeamYears'])
            teams = teams['TeamYears']
            # Add column ABBREVIATION to the dataset
            teams_dataset["ABBREVIATION"] = teams_dataset.merge(teams, on="TEAM_ID")["ABBREVIATION"]
            # Add column YEARFOUNDED to the dataset
            teams_dataset['YEARFOUNED'] = teams_dataset.merge(teams, on="TEAM_ID")['MIN_YEAR']

            return teams_dataset
        except Exception as e:
            raise e
    

# NBA Url for team lineup
# https://stats.nba.com/stats/leaguedashlineups?Conference=&DateFrom=&DateTo=&Division=&GameID=&GameSegment=&GroupQuantity=5&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlusMinus=N&Rank=N&Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&TeamID=0&VsConference=&VsDivision=

# NBA Url for teams stats per season
# https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=

# NBA Url for Team scorboard per season
# https://stats.nba.com/stats/leaguegamelog?Counter=1000&DateFrom=&DateTo=&Direction=DESC&LeagueID=00&PlayerOrTeam=T&Season=2021-22&SeasonType=Regular+Season&Sorter=DATE

