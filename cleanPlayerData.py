#!usr/bin/env python3
import pandas as pd
import numpy as np

scores = {
	

	'draftkings' : {

					'tov' : -.50,
					'pts' : 1,
					'fg3' : .50,
					'trb' : 1.25,
					'ast' : 1.50,
					'stl' : 2,
					'blk' : 2,
					'dd' : 1.5,
					'td' : 3

		    		}

}


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


def shift_columns(df, columns, shifts, averages):

    for column in columns:
        for shift in shifts:
            df[column + str(shift)] =  df.groupby('player')[column].shift(periods=shift)

        for average in averages:
            selector = [column + str(x) for x in range(-1, average-1, -1)]
            df[column + str(average) + 'avg'] = df.loc[:,selector].mean(axis=1)

        for shift in shifts:
            del df[column +str(shift)]

        df.sort_values(by=['date_game', 'player'], inplace=True)
    
        df[column + 'seasonavg'] = df.groupby('player')[column].apply(
            lambda x: pd.expanding_mean(x).shift())

    df['rest'] = df.groupby('player')['date_game'].diff().astype('timedelta64[D]')

    return df


def remove_last_row(group):
    
    return group.iloc[0 : -1, : ]


def apply_transformers(df, **kwargs):

        
        for key, value in kwargs.items():
        	
            if value[0]:    
                df[key] = df[value[0]].apply(value[1]) 
            
            else:
                df[key] = df.apply(value[1], axis=1)

        return df


def calculate_score(df, col_name, **kwargs):

	df[col_name] = 0
	for key, value in kwargs.items():
		df[col_name] += df[key] * value

	return df


def clean_double_double(row):

	stats = ['pts', 'trb', 'ast', 'stl', 'blk']
	count = 0

	for stat in stats:

		if row[stat] >= 10:
			count += 1

	if count >= 2:
		return 1
	else:
		return 0


def clean_triple_double(row):

	stats = ['pts', 'trb', 'ast', 'stl', 'blk']
	count = 0

	for stat in stats:

		if row[stat] >= 10:
			count += 1

	if count >= 3:
		return 1
	else:
		return 0	


def main():
    pass


if __name__ == '__main__':
    main()
    
    playerDF = pd.read_csv('player_data.csv',
                    
                    index_col=0,
                    parse_dates=['date_game'],
                    infer_datetime_format=True,
                    converters={
                        'age' : clean_age_column,
                        'game_location' : clean_game_location_column,},
                        )

    transformers = 	{
        			'primary_position' : ('pos', clean_pos_column_primary),
        			'secondary_position' : ('pos', clean_pos_column_secondary),
        			'dd' : (None, clean_double_double),
        			'td' : (None, clean_triple_double),
        			}
    
    playerDF = apply_transformers(playerDF, **transformers)

    for score_dict in scores:

    	playerDF = calculate_score(playerDF, score_dict, **scores[score_dict])

    playerDF.sort_values(by=['date_game', 'player'],
                         ascending=False,
                         inplace=True)

    metrics = [col for col in playerDF.columns if playerDF.dtypes[col]
               in [int, float]]

    shifts = [-1, -2, -3, -4, -5,-6, -7, -8, -9, -10]

    averages = [-3, -5, -7, -10]

    playerDF = shift_columns(playerDF, metrics, shifts, averages)

    playerDF = playerDF.groupby('player', group_keys=False).apply(remove_last_row)

    playerDF.fillna(0, inplace=True)

    playerDF.to_csv('clean_player_data.csv')
