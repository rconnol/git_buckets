#!/usr/bin/env python3
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


def initialize_web_driver(url, offset):

    driver = webdriver.Firefox()

    driver.get(url + str(offset))

    html = driver.page_source

    table_exists = True

    try:
        driver.find_element_by_id('stats')
    except:
        print('End of Stats')
        table_exists = False

    driver.quit()

    return html, table_exists


def read_br_tables():

    url = ("http://www.basketball-reference.com/play-index/pgl_finder.cgi?"
       "request=1&player_id=&match=game&year_min=2017&year_max=2017&ag"
       "e_min=0&age_max=99&team_id=&opp_id=&is_playoffs=N&round_id=&ga"
       "me_num_type=&game_num_min=&game_num_max=&game_month=&game_day="
       "&game_location=&game_result=&is_starter=&is_active=&is_hof=&po"
       "s_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is"
       "_c=Y&pos_is_cf=Y&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val="
       "&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&is_dbl_dbl=&is_"
       "trp_dbl=&order_by=pts&order_by_asc=&offset=")
    
    offset = 0
    table_exists = True
    
    data = []
    while table_exists:
        
        page, table_exists = initialize_web_driver(url, offset)

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
        
            data.append(info)

        offset += 100

    return data


def main():
    
    data = read_br_tables(url)

    playerDF = pd.DataFrame(data)

    playerDF.dropna(how='all', inplace=True)

    playerDF.to_csv('player_data.csv')


if __name__ == '__main__':
    main()