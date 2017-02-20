#!/usr/bin/env python3
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

        tabularize_webpage: returns a DataFrame of the Basketball Reference 
                            web scraped data.

    """ 
   
    url_api = ("http://www.basketball-reference.com/play-index/pgl_finder.cgi?"
       "request=1&player_id=&match=game&year_min={}&year_max={}&ag"
       "e_min=0&age_max=99&team_id=&opp_id=&is_playoffs=N&round_id=&ga"
       "me_num_type=&game_num_min=&game_num_max=&game_month=&game_day="
       "&game_location=&game_result=&is_starter=&is_active=&is_hof=&po"
       "s_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is"
       "_c=Y&pos_is_cf=Y&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val="
       "&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&is_dbl_dbl=&is_"
       "trp_dbl=&order_by=pts&order_by_asc=&offset={}")

    
    def __init__(self, min_year=2017, max_year=2017, offset=0):

        self.min_year = min_year
        self.max_year = max_year
        self.offset = offset
        self.url = self.url_api.format(
                                  str(self.min_year),
                                  str(self.max_year),
                                  str(self.offset)
                                  )

    
    def api_constructor(self):

        self.url = self.url_api.format(
                                  str(self.min_year),
                                  str(self.max_year),
                                  str(self.offset)
                                  )
        return self.url
    
    def initialize_page(self):

        url = self.api_constructor()

        driver = webdriver.Firefox()

        driver.get(url)
        
        html = driver.page_source

        table_exists = True

        try:
            driver.find_element_by_id('stats')
        except:
            print('End of Stats')
            table_exists = False

        driver.quit()

        return html, table_exists


    def tabulate_webpage(self, csv=True):

        self.data = []
        self.csv = csv

        while True:

            page, table_exists = self.initialize_page()

            if not table_exists:
                break

            soup = BeautifulSoup(page, 'lxml')
            table = soup.find(id='stats')
            rows = table.findChildren('tr')
            
            for row in rows:
                info = {}
                cells = row.findChildren('td')

                for cell in cells:
                    info[cell['data-stat']] = cell.text
            
                self.data.append(info)

            self.offset += 100

        df = pd.DataFrame(self.data)

        df.dropna(how='all', inplace = True)

        if csv:
            df.to_csv('player_data.csv')

        return df
    

def main():
    scraper = BasketballReference()
    data = scraper.tabulate_webpage(csv=True)


if __name__ == '__main__':
    main()    


# def initialize_web_driver(url, offset):

#     driver = webdriver.Firefox()

#     driver.get(url + str(offset))

#     html = driver.page_source

#     table_exists = True

#     try:
#         driver.find_element_by_id('stats')
   
#     except:
#         print('No stats on Page')
#         table_exists = False

#     driver.quit()

#     return html, table_exists


# def read_br_tables():

#     url = ("http://www.basketball-reference.com/play-index/pgl_finder.cgi?"
#        "request=1&player_id=&match=game&year_min=2017&year_max=2017&ag"
#        "e_min=0&age_max=99&team_id=&opp_id=&is_playoffs=N&round_id=&ga"
#        "me_num_type=&game_num_min=&game_num_max=&game_month=&game_day="
#        "&game_location=&game_result=&is_starter=&is_active=&is_hof=&po"
#        "s_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is"
#        "_c=Y&pos_is_cf=Y&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val="
#        "&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&is_dbl_dbl=&is_"
#        "trp_dbl=&order_by=pts&order_by_asc=&offset=")
    
#     offset = 0
#     table_exists = True
    
#     data = []
#     while table_exists:
        
#         page, table_exists = initialize_web_driver(url, offset)

#         if not table_exists:
#             break

#         soup = BeautifulSoup(page, 'lxml')
#         table = soup.find(id='stats')
#         rows = table.findChildren('tr')
        
#         for row in rows:
#             info = {}
#             cells = row.findChildren('td')

#             for cell in cells:
#                 info[cell['data-stat']] = cell.text
        
#             data.append(info)

#         offset += 100

#     return data


# def main():
    
#     data = read_br_tables(url)

#     playerDF = pd.DataFrame(data)

#     playerDF.dropna(how='all', inplace=True)

#     playerDF.to_csv('player_data.csv')


# if __name__ == '__main__':
#     pass
#     #main()