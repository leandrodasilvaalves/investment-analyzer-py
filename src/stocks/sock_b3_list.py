import os

import pandas as pd
import requests


def get_list():
    file = "csv_files/acoes_b3.csv"
    if(os.path.exists(file)):
        print('retornando arquivo local: ', file)
        return pd.read_csv(file)

    API_KEY = os.getenv("TWELVE_DATA_API_KEY")
    BASE_URL = "https://api.twelvedata.com/stocks"
    B3_CODE = "BVMF"

    params = { "exchange": B3_CODE, "apikey": API_KEY, }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data["data"])
        df.to_csv(file, index=False)
        print(f"Lista de ações salva como '{file}'")
        return df
    
    else:
        print(f"Erro ao acessar a API: {response.status_code} - {response.text}")
