import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

def page_to_soup(page, parser='lxml'):

	page = urlopen(page)
	soup = BeautifulSoup(page, parser)
	page.close()

	return soup		


def main():

	soup = page_to_soup('http://rotoguru1.com/cgi-bin/nba-dhd-2017.pl')
	rows = soup.find_all('pre')

	#turn the soup into text split at every new line
	text = str(rows).split('\n')
	
	#remove the first six irrelevant characters of the first line
	text[0] = text[0][6:]

	#remove the last irrelevant items in the list
	for i in range(0,2):
		text.pop()

	#the first row is the list of column headers
	header = text.pop(0)
	header = header.split(':')

	data = []
	for row in text:
		player = {}
		for key, value in zip(header, row.split(':')):
			player[key] = value
		
		data.append(player)
	
	return data


if __name__ == '__main__':
	data = main()