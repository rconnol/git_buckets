#!/usr/bin/env python3
import urllib.parse
import sys
import pdb
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


class BasketballReference(object):

    
    """BasketballReference.com scraper, using their url API.
    The scraper has the following properties:

    Global Attributes:
        
        url_api: Is the url api with query markers set.
                 Using the .format method to complete url.

    Attributes:

        min_year: Is the minimum season year for BasketballReference query.
        max_year: Is the maximum season year for BasketballReference query.
        offset: Pagination Handler.
    
    Methods:

        tabulate_webpage: returns a DataFrame of the Basketball Reference 
                          web scraped data.

    """ 


    def __init__(self):
        
        self.url_base = "http://www.basketball-reference.com/"\
                        "play-index/pgl_finder.cgi?"

        self.url_query = {
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


    def tabulate_webpage(self):

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
    

def main():
    scraper = BasketballReference()
    bballrefDF = scraper.tabulate_webpage()
    
    try:
        data.to_csv(sys.argv[1])
    except:
    	pass

    return bballrefDF


if __name__ == '__main__':
    bballrefDF = main()