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


def engineer_all(df):

    df['dd'] = df.apply(engineer_double_double, axis=1)

    df['td'] = df.apply(engineer_triple_double, axis=1)

    df = engineer_days_of_rest(df)

    df = engineer_fantasy_scores(df, fantasy_score_multipliers)

    df = engineer_previous_game_averages(

            df=df,
            columns = [col for col in df if df.dtypes[col] in [int, float]],
            previous_game_averages = range(1,16,2)
            
            )

    return df


def engineer_double_double(row):

    stats = ['pts', 'trb', 'ast', 'stl', 'blk']
    count = 0

    for stat in stats:

        if row[stat] >= 10:
            count += 1

    if count >= 2:
        return 1
    else:
        return 0


def engineer_triple_double(row):

    stats = ['pts', 'trb', 'ast', 'stl', 'blk']
    count = 0

    for stat in stats:

        if row[stat] >= 10:
            count += 1

    if count >= 3:
        return 1
    else:
        return 0


def engineer_days_of_rest(df):

    df.sort_values(by=['date_game', 'player'], inplace=True)
    
    df['rest'] = df.groupby(
        'player')['date_game'].diff().astype('timedelta64[D]')

    df['rest'] = df['rest'] - 1

    return df


def engineer_fantasy_scores(df, fantasy_score_multipliers):

    for column in fantasy_score_multipliers:

        df[column] = 0
        
        for game_stat in fantasy_score_multipliers[column]:
            
            df[column] += (df[game_stat] *
                           fantasy_score_multipliers[column][game_stat])

    return df


def engineer_previous_game_averages(df, columns, previous_game_averages):   

    for column in columns:

        df.sort_values(by=['date_game', 'player'],
                       ascending=True,
                       inplace=True) 

        for offset in range(1, max(previous_game_averages) + 1):
            
            df[column + "-" + str(offset)] =  df.groupby(
                'player')[column].shift(periods=offset)

        for average in previous_game_averages:
            
            selector = [column + "-" + str(x) for x in range(1, average + 1)]
            df[column + str(average) + 'game-avg'] = df.loc[:,selector].mean(axis=1)

        for offset in range(1, max(previous_game_averages) + 1):
            
            del df[column + "-" + str(offset)]

        df[column + 'seasonavg'] = df.groupby('player')[column].apply(
            lambda x: pd.expanding_mean(x).shift())

    return df


fantasy_score_multipliers = {
        

        'draftkings' : {

                        'ast' : 1.50,
                        'blk' : 2,
                        'dd' : 1.5,
                        'fg3' : .50,
                        'pts' : 1,
                        'stl' : 2,
                        'td' : 3,
                        'tov' : -.50,
                        'trb' : 1.25,
                        
                        },


        'fanduel' : {

                        'ast' : 1.50,
                        'blk' : 2,
                        'dd' : 0,
                        'fg3' : 0,
                        'pts' : 1,
                        'stl' : 2,
                        'td' : 0,
                        'tov' : -1,
                        'trb' : 1.20,
                        
                        },

        'yahoo' : {

                        'ast' : 1.50,
                        'blk' : 2,
                        'dd' : 0,
                        'fg3' : .5,
                        'pts' : 1,
                        'stl' : 2,
                        'td' : 0,
                        'tov' : -1,
                        'trb' : 1.20,
                        
                        },
    }


if __name__ == '__main__':
    
    playerDF = pd.read_csv('player_stats.csv',
                
                index_col=0,
                parse_dates=['date_game'],
                infer_datetime_format=True,
                converters={
                    
                    'age' : clean_age,
                    'game_location' : clean_game_location,
                    
                    })

    playerDF.fillna(0, inplace=True)
    playerDF = engineer_all(playerDF)
    playerDF.dropna(how='any', inplace=True)
    playerDF.to_csv('clean_player_stats.csv')