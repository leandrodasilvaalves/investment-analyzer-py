import yfinance as yf
from datetime import datetime, timedelta
import os
import pandas as pd
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import csv_files

INTERVAL_DAYS = 365

def parse_result(data):
    data_list = data.reset_index().to_dict(orient='records')    
    df = pd.DataFrame(data_list)
    
    new_column_names = {}
    for col in df.columns:
        if isinstance(col, tuple):
            new_column_names[col] = col[0] 
        else:
            new_column_names[col] = col

    df.rename(columns=new_column_names, inplace=True)
    df = df.round(2)
    
    return df

def get_history_from_yahoo(start_date, end_date, asset):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    print('obtendo dados do "yahoo finances"')
    data = yf.download(f"{asset}.SA", start=start_date_str, end=end_date_str)
    return parse_result(data)


def get_history(asset):        
    end_date = datetime.today()
    start_date = end_date - timedelta(days=INTERVAL_DAYS)
    
    file = csv_files.build_file_name(asset)
    
    if(os.path.exists(file)):
        print('retornando arquivo local: ', file)
        historical_data = pd.read_csv(file)
        outdated_file, new_start_date = csv_files.verify_file_data(start_date, end_date, historical_data)
        
        if(outdated_file):
            new_historical_data = get_history_from_yahoo(new_start_date, end_date, asset)
            new_historical_data.to_csv(file, mode='a', header=False, index=False)
            historical_data = pd.concat([historical_data, new_historical_data], ignore_index=True)

    else:
        historical_data = get_history_from_yahoo(start_date, end_date, asset)
        historical_data.to_csv(file, index=False)

    if 'Date' in historical_data.columns:
        historical_data['Date'] = pd.to_datetime(historical_data['Date']).dt.strftime('%Y-%m-%d')
        
    return historical_data     