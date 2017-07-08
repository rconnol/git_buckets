import pandas as pd

def prefix_columns(df, string):

	df.columns = [string + col for col in df.columns]

	return df


columns_to_remove = ['age', 'ast', 'blk', 'drb', 'fg', 'fg2', 'fg2_pct', 'fg2a',
'fg3', 'fg3_pct', 'fg3a', 'fg_pct', 'fga', 'ft', 'ft_pct', 'fta','game_result', 
'game_score', 'mp', 'orb', 'pf', 'pts', 'stl', 'tov', 'trb', 'dd',
'td', 'draftkings', 'fanduel', 'yahoo', 'opp_fg', 'opp_fg2', 'opp_fg2_pct',
'opp_fg2a', 'opp_fg3', 'opp_fg3_pct', 'opp_fg3a', 'opp_fg_pct',
'opp_fga', 'opp_ft', 'opp_ft_pct', 'opp_fta', 'opp_pts', 'pts']


def remove_columns(df, cols):

	for col in cols:

		try:
			del df[col]

		except KeyError:
			pass

	return df


if __name__ == '__main__':
	
	teamDF = pd.read_csv('clean_team_stats.csv')
	playerDF = pd.read_csv('clean_player_stats.csv')

	teamDF = remove_columns(teamDF, columns_to_remove)
	playerDF = remove_columns(playerDF, columns_to_remove)

	orginal_column_names = teamDF.columns

	team_teamDF = prefix_columns(teamDF, 'team_')
	mergedDF = playerDF.merge(team_teamDF,
		                      how='left',
			                  left_on=['team_id', 'date_game'],
		                      right_on=['team_team_id', 'team_date_game'])
	

	teamDF.columns = orginal_column_names
	opp_teamDF = prefix_columns(teamDF, 'opp_')
	mergedDF = mergedDF.merge(opp_teamDF, 
						      how='left',
		                      left_on=['opp_id', 'date_game'],
		                      right_on=['opp_team_id', 'opp_date_game'])