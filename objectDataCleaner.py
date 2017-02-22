#!usr/bin/env python3
import pandas as pd
import numpy as np

class BasketballReferenceDataCleaner(object):

	def __init__(self, filename='player_data.csv'):

		self.filename = filename
		self.df = pd.read_csv(filename).fillna(0)

if __name__ == '__main__':
	
	data = BasketballReferenceDataCleaner()