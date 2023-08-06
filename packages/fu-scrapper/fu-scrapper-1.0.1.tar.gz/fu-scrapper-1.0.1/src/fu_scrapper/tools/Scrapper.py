import requests
from time import sleep


class Scrapper():
    """
    Class to simplify scrapping on website and API.

    """
    HEADER = {
        'Host': 'stats.nba.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Referer': 'https://www.nba.com/stats/',
        'Origin': 'https://www.nba.com',
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
    }

    def __init__(self, max_call_errors=None):
        self.max_call_errors = max_call_errors

    def repeat_call_while_error(self, url):
        response = requests.get(url, headers=self.HEADER)
        errors_cnt = 0
        while not response.status_code != 200 & errors_cnt < self.max_call_errors:
            sleep(1)
            errors_cnt += 1
            response = requests.get(url, headers=self.HEADER)

        if errors_cnt == self.max_call_errors:
            return None

        return response

    def call_url(self, url):
        self.HEADER['Referer'] = url
        
        response = requests.get(url, headers=self.HEADER)

        if response.status_code != 200:
            if self.max_call_errors != None:
                response = self.repeat_call_while_error(url=url)

            if response == None:
                return None

        return response

    def retrieve_json_api_from_url(self, url):
        response = self.call_url(url=url)

        if response == None:
            return None

        if response.status_code != 200:
            print('Error code : %i'%response.status_code)
            return None

        return response.json()
