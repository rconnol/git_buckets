#!usr/bin/env python3
import pandas as pd
import numpy as np

# class PlayerData(object):
# 	"""A pd.DataFrame of data scraped from Basketball-Reference
# 	Different Parameters for scraping data.
# 	"""
# 	url = 

# 	def __init__(self, df):
# 		self.df = df

def clean_age_column(cell):

	years = cell[ : 2]
	days = cell[3 : ]
	age = int(years) + int(days)/365

	return age


def clean_game_location_column(cell):

	if cell == '@':
		return 'Away'
	else:
		return 'Home'


def clean_pos_column_primary(cell):

	if len(cell) == 3:
		primary_position = cell[0 : 1]
	if len(cell) < 3:
		primary_position = cell

	return primary_position


def clean_pos_column_secondary(cell):

	if len(cell) == 3:
		secondary_position = cell[2 : 3]
	if len(cell) < 3:
		secondary_position = 'None'

	return secondary_position


def calculate_draftkings_score(row):

	fantasy_points = 0

	fantasy_points += row['pts']

	fantasy_points += row['fg3']*.50

	fantasy_points += row['trb']*1.25

	fantasy_points += row['ast']*1.50

	fantasy_points += row['stl']*2

	fantasy_points += row['blk']*2

	fantasy_points += row['tov']*-.50

	count = 0
	for stat in ['pts', 'trb', 'ast', 'stl', 'blk']:
		if row[stat] > 10:
			count += 1

	if count == 2:
		fantasy_points += 1.5

	if count == 3:
		fantasy_points += 3

	return fantasy_points


def shift_columns(df, columns, shifts, averages):

	for column in columns:
		for shift in shifts:
			df[column + str(shift)] =  df.groupby('player')[column].shift(periods=shift)

	for column in columns:
		for average in averages:
			selector = [column + str(x) for x in range(-1, average-1, -1)]
			df[column + str(average) + 'avg'] = df.loc[:,selector].mean(axis=1)

	for column in columns:
		for shift in shifts:
			del df[column +str(shift)]

	df.sort_values(by=['date_game', 'player'], inplace=True)
	for column in columns:
		df[column + 'seasonavg'] = df.groupby('player')[column].apply(
			lambda x: pd.expanding_mean(x).shift())

	df['rest'] = df.groupby('player')['date_game'].diff().astype('timedelta64[D]')

	df.sort_values(by=['date_game', 'player'],
	                 ascending=False,
	                 inplace=True)

	return df


def remove_last_row(group):
	return group.iloc[0 : -1, : ]


def main():
	pass



if __name__ == '__main__':
	main()
	
	playerDF = pd.read_csv('player_data.csv', index_col=0)

	playerDF.fillna(0, inplace=True)
	
	playerDF['age'] = playerDF['age'].apply(clean_age_column)
	
	playerDF['game_location'] = playerDF['game_location'].apply(
		clean_game_location_column)

	playerDF['primary_position'] = playerDF['pos'].apply(
		clean_pos_column_primary)

	playerDF['secondary_position'] = playerDF['pos'].apply(
		clean_pos_column_secondary)

	del playerDF['pos']

	playerDF['date_game'] = pd.to_datetime(playerDF['date_game'])

	playerDF['draftkings'] = playerDF.apply(calculate_draftkings_score, axis=1)

	playerDF.sort_values(by=['date_game', 'player'],
		                 ascending=False,
		                 inplace=True)


	metrics = ['ast', 'blk', 'drb', 'fg', 'fg2', 'fg2_pct', 'fg2a',
	           'fg3', 'fg3_pct', 'fg3a', 'fg_pct', 'fga', 'ft',
	           'ft_pct', 'fta', 'mp', 'orb', 'pf', 'pts', 'stl', 'tov', 'trb']

	shifts = [-1, -2, -3, -4, -5,-6, -7, -8, -9, -10]

	averages = [-3, -5, -7, -10]

	playerDF = shift_columns(playerDF, metrics, shifts, averages)

	playerDF = playerDF.groupby('player', group_keys=False).apply(remove_last_row)

	playerDF.to_csv('clean_player_data.csv')
