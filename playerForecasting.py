import pandas as pd

def main():
	pass


if __name__ == '__main__':
	main()

	playerDF = pd.read_csv('clean_player_data.csv', index_col=0)

	metrics = ['ast', 'blk', 'drb', 'fg', 'fg2', 'fg2_pct', 'fg2a',
	           'fg3', 'fg3_pct', 'fg3a', 'fg_pct', 'fga', 'ft',
	           'ft_pct', 'fta', 'orb', 'pf', 'pts', 'stl', 'tov', 'trb']

	forecasting_columns = [column for column in playerDF.columns if
	                       column not in metrics]

	forecastingDF = playerDF.loc[:, forecasting_columns]