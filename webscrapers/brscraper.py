#!/usr/bin/env python3
import urllib.parse
import sys
import pandas as pd
from enum import Enum
from bs4 import BeautifulSoup
from selenium import webdriver



class BasketballReference(object):

    
    """BasketballReference.com scraper, using their url API.
    The scraper has the following properties:
    
    Methods:

        scrape_webpage: returns a DataFrame of the Basketball Reference 
                          web scraped data.

    """ 


    def __init__(self, url, url_query):
        
        self.url_base = url

        self.url_query = url_query

        self.url = self.url_base + urllib.parse.urlencode(self.url_query)                         

    
    def api_constructor(self):

        self.url = self.url_base + urllib.parse.urlencode(self.url_query)
        
        return self.url
    

    def get_page(self, driver):
        #don't want to initialize driver in __init__
        #opens blank webpage upon initialization

        url = self.api_constructor()

        driver.get(url)
        
        html = driver.page_source

        table_exists = True

        try:
            driver.find_element_by_id('stats')
        except:
            print('End of Stats')
            table_exists = False

        return html, table_exists


    def scrape_webpage(self):

        data = []

        driver = webdriver.Firefox()

        while True:

            page, table_exists = self.get_page(driver=driver)

            if not table_exists:
                break

            #lxml is parser for webpage'
            soup = BeautifulSoup(page, 'lxml')
            
            table = soup.find(id='stats')
            
            rows = [row for row in table.findChildren('tr') if 'data-row'
                    in row.attrs and 'class' not in row.attrs]
            
            for row in rows:
                cells = row.findChildren('td')
                info = {cell['data-stat'] : cell.text for cell in cells}
            
                data.append(info)

            self.url_query['offset'] += 100

        driver.quit()

        df = pd.DataFrame(data)

        return df


playerGame_url = "http://www.basketball-reference.com/" \
                 "play-index/pgl_finder.cgi?"


playerGame_query = {
                   'request' : 1,
                   "player_id" : '',
                   "match" : 'game',
                   "year_min" : 2017,
                   "year_max" : 2017,
                   "age_min" : 0,
                   "age_max" : 99,
                   "team_id" : '',
                   "opp_id" : '',
                   "is_playoffs" : 'N',
                   "round_id" : '',
                   "game_num_type" : '',
                   "game_num_min" : '',
                   "game_num_max" : '',
                   "game_month" : '',
                   "game_day" : '',
                   "game_location" : '',
                   "game_result" : '',
                   "is_starter" : '',
                   "is_active" : '',
                   "is_hof" : '',
                   "pos_is_g" : 'Y',
                   "pos_is_gf" : 'Y',
                   "pos_is_f" : "Y",
                   "pos_is_fg" : "Y",
                   "pos_is_fc" : "Y",
                   "pos_is_c" : "Y",
                   "pos_is_cf" : "Y",
                   "c1stat" : '',
                   "c1comp" : '',
                   "c1val" : '',
                   "c2stat" : '',
                   "c2comp" : '',
                   "c2val" : '',
                   "c3stat" : '',
                   "c3comp" : '',
                   "c3val" : '',
                   "c4stat" : '',
                   "c4comp" : '',
                   "c4val" : '',
                   "is_dbl_dbl" : '',
                   "is_trp_dbl" : '',
                   "order_by" : 'pts',
                   "order_by_asc" : '',
                   "offset" : 0,
                  }


teamGame_url = "http://www.basketball-reference.com/" \
               "play-index/tgl_finder.cgi?"


teamGame_query = {
                  'request' : 1,
                  'match' : 'game',
                  'lg_id' : 'NBA',
                  'is_playoffs' : 'N',
                  'team_seed_cmp' : 'eq',
                  'opp_seed_cmp' : 'eq',
                  'year_min' : 2017,
                  'year_max' : 2017,
                  'is_range' : 'N',
                  'game_num_type' : 'team',
                  'player': '',
                  'team_id' : '',
                  'opp_id' : '',
                  'round_id' : '',
                  'best_of' : '',
                  'team_seed' : '',
                  'opp_seed' : '',
                  'game_num_min' : '',
                  'game_num_max' : '',
                  'game_month' : '',
                  'game_location' : '',
                  'game_result' : '',
                  'is_overtime' : '',
                  'c1stat' : '',
                  'c1comp' : '',
                  'c1val' : '',
                  'c2stat' : '',
                  'c2comp' : '',
                  'c2val' : '',
                  'c3stat' : '',
                  'c3comp' : '',
                  'c3val' : '',
                  'c4stat' : '',
                  'c4comp' : '',
                  'c4val' : '',
                  'order_by' : 'pts',
                  'order_by_asc' : '',
                  'offset' : 0,
                  }

class QueryType(Enum):
    TEAM = [teamGame_url, teamGame_query]
    PLAYER = [playerGame_url, playerGame_query]


def main():

    #scrape the data
    team_game = BasketballReference(*QueryType.TEAM.value)
    player_game = BasketballReference(*QueryType.PLAYER.value)

    #scrape Basketball Reference return DataFrame
    team_gameDF = team_game.scrape_webpage()
    player_gameDF = player_game.scrape_webpage()

    #pandas.DataFrame.to_csv
    team_gameDF.to_csv('~/fantasyNBA/team_stats.csv')
    player_gameDF.to_csv('~/fantasyNBA/player_stats.csv')

    return team_gameDF, player_gameDF


if __name__ == '__main__':
    
    team_gameDF, player_gameDF = main()