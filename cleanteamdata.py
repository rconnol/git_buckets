#!usr/bin/env python3
import pandas as pd
import numpy as np


def clean_age(cell):

    years = cell[ : 2]
    days = cell[3 : ]
    age = int(years) + int(days)/365

    return age


def clean_game_location(cell):

    if cell == '@':
        return 'Away'
    else:
        return 'Home'

def clean_game_result(cell):

	return cell.split()[0]


def engineer_all(df):

	df = engineer_previous_game_averages(

		df=df,
		columns = [col for col in df if df.dtypes[col] in [int, float]],
		previous_game_averages = range(1,16,2)

		)

	return df


def engineer_previous_game_averages(df, columns, previous_game_averages):   

    for column in columns:

        df.sort_values(by=['date_game', 'team_id'],
                       ascending=True,
                       inplace=True) 

        for offset in range(1, max(previous_game_averages) + 1):
            
            df[column + "-" + str(offset)] =  df.groupby(
                'team_id')[column].shift(periods=offset)

        for average in previous_game_averages:
            
            selector = [column + "-" + str(x) for x in range(1, average + 1)]
            df[column + str(average) + 'game-avg'] = df.loc[:,selector].mean(axis=1)

        for offset in range(1, max(previous_game_averages) + 1):
            
            del df[column + "-" + str(offset)]

        df[column + 'seasonavg'] = df.groupby('team_id')[column].apply(
            lambda x: pd.expanding_mean(x).shift())

    return df


if __name__ == '__main__':
    
    teamDF = pd.read_csv('team_stats.csv',
                
                index_col=0,
                parse_dates=['date_game'],
                infer_datetime_format=True,
                converters={
                    
                    'age' : clean_age,
                    'game_location' : clean_game_location,
                    'game_result' : clean_game_result,

                    })

    teamDF.fillna(0, inplace=True)
    teamDF = engineer_all(teamDF)
    teamDF.dropna(how='any', inplace=True)
    teamDF.to_csv('clean_team_stats.csv')