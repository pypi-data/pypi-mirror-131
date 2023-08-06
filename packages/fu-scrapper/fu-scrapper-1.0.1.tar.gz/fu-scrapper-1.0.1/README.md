# FU-Scrapper

![PyPI](https://img.shields.io/pypi/v/fu_scrapper?label=Version&style=plastic) ![GitHub](https://img.shields.io/github/license/endy02/fu-scrapper?style=plastic) ![GitHub top language](https://img.shields.io/github/languages/top/endy02/fu-scrapper?style=plastic) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/endy02/fu-scrapper?color=%23f16d18&style=plastic)

---
> This package allow you to get data in csv format optimized for data analysis

Python tool that can save you a lot of time in research and modeling data for analysis. Here you can extract data from any listed source like NBA data and put it into a csv file.

---
### Features
> <b>NBA api</b>
- Player stats data
- Team stats data
- Game stats data
- Game details stats data
- Ranking data

> More comming soon ...



---


### Installation
Use python package manager to install fu-scrapper (<b>pip</b>) :
<b>
```
pip install fu-scrapper
```
</b>

> You can find this package available on PyPi <a href="https://pypi.org/project/fu-scrapper/"> here</a>.

---


### Usage

Initialize the source that you need and use the functions provided by the package :

```python
# import and precise the source
# in our case it's nba
from fu-scrapper.nba.players import Players
from fu-scrapper.nba.teams import Teams

if __name__ = '__main__':
    # Player class instantiation
    players = Players()
    # All players general stats into csv file
    players.extract_players()

    # team class instantiation
    teams = Teams()
    # All teams total stats into csv file
    teams.extract_teams_details()
```

---

### Functions

> <b>NBA Api</b>

| function | descritpion |
| --- | --- |
| ``` players.extract_players() ``` | Extract all players informations and global stats for the current season into a csv file |
| ``` teams.extract_teams() ``` |  Extract all teams informations and global stats for the current season into a csv file |
| ``` teams.extract_teams_details() ``` | Extract all teams details by games |
| ``` games.next_week_games() ``` | Get informations of all next week games into csv file |
| ``` games.last_week_games() ``` | Get all last week game details |
| ``` games.today_games() ``` | Get listing of today games into csv file |
| ``` games.new_games() ``` | Get all new game stats and ranking into a csv file |

---

### License

Copyright (c) 2021 Fujyn <br>
Licensed under the <a href="https://github.com/Endy02/fu-scrapper/blob/master/README.md">MIT license</a>.

---

### Contributing

<b>Bugs & New Features</b>

Please use the <a href="https://github.com/Endy02/fu-scrapper/issues">issue tracker</a> to report any bugs or feature requests.