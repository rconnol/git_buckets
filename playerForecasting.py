import pandas as pd
import solar_corr

def main():
	pass


if __name__ == '__main__':
	main()

	playerDF = pd.read_csv('clean_player_data.csv', index_col=0)

	exclude_columns = ['ast', 'blk', 'date_game', 'drb', 'fg', 'fg2',
	                   'fg2_pct', 'fg2a', 'opp_id', 'player', 'team_id',
	                   'fg3', 'fg3_pct', 'fg3a', 'fg_pct', 'fga', 'ft',
	                   'ft_pct', 'fta', 'game_result', 'game_score',
	                   'mp', 'orb', 'pf', 'pts', 'stl', 'tov', 'trb']

	forecasting_columns = [column for column in playerDF.columns if
	                       column not in exclude_columns]

	forecastingDF = playerDF.loc[:, forecasting_columns]

	forecastingDF = pd.get_dummies(forecastingDF)

	forecastingDF.to_csv('forecasting_stats.csv', index=False)

	solar_corr.main('forecasting_stats.csv', 'draftkings', 'nba_solar.csv')