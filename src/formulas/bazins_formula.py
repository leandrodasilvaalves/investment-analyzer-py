import os
import sys
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import csv_files

def fetch_financial_data(ticker):
    if ticker.endswith("34"):
        print(f"BDR detectado: {ticker} - Ignorando...")
        return None

    try:
        print(f"obtentado dados de {ticker}")

        stock = yf.Ticker(f"{ticker}.SA")
        info = stock.info

        market_cap = info.get("marketCap", np.nan)
        debt = info.get("totalDebt", np.nan)
        cash = info.get("totalCash", np.nan)
        ebitda = info.get("ebitda", np.nan)
        avg_volume_10d = info.get("averageDailyVolume10Day", np.nan)
        sector = info.get("sector", "Unknown")

        enterprise_value = calculate_ev(market_cap, debt, cash)
        ev_ebitda = caculdate_ev_ebitda(enterprise_value, ebitda)

        return {
            "Ticker": ticker,
            "Market Cap": market_cap,
            "Debt": debt,
            "Cash": cash,
            "EBITDA": ebitda,
            "Enterprise Value": enterprise_value,
            "EV/EBITDA": ev_ebitda,
            "Avg Volume 10D": avg_volume_10d,
            "Sector": sector,
        }
    except Exception as e:
        print(f"Erro ao buscar dados para {ticker}: {e}")
        return None
    
def calculate_ev(market_cap, debt, cash):
    return market_cap + debt - cash if not np.isnan(market_cap) else np.nan

def caculdate_ev_ebitda(enterprise_value, ebitda):
    return enterprise_value / ebitda if not np.isnan(enterprise_value) and ebitda else np.nan

def get_stocks_with_greater_liquidity(df):
    return df[df["Avg Volume 10D"] >= 200_000]

def remove_financial_sectors(df):
    excluded_sectors = ["Financial Services", "Insurance", "Banks"]
    return df[~df["Sector"].isin(excluded_sectors)]

def add_ticker_base_column(df):
    df['Ticker Base'] = df['Ticker'].apply(lambda x: x[:-1] if x[-1].isdigit() else x)
    return df

def remove_duplicate_ticker_base(df):
    idx_max_volume = df.groupby('Ticker Base')['Avg Volume 10D'].idxmax()
    return df.loc[idx_max_volume]

def order_by_ev_ebitda(df):
    return df.sort_values(by="EV/EBITDA", ascending=True)

def save_file():
    csv_files.build_file_name("ranking_bazin", datetime.now().strftime("%Y-%m-%d"))

def log_warnings():
    print("\n\nATENÇÃO!!!")
    print("Você ainda deve verificar manualmente:")
    print('- se a empresta está em recuperação judicial. Você pode fazer isso clicando no link da empresa no investsite e verificar campo "Situação Emissor"')
    print("- remover empresas cujo resultado operacional está inflacionado. Por exemplo vendeu uma filia rescentemente")
    print("- remover empresas que tenha notícias recentes de envolvimento em escândalos.")


def process_formula(tickers):
    data = [fetch_financial_data(ticker) for ticker in tickers]
    df = pd.DataFrame(filter(None, data))
    
    df = get_stocks_with_greater_liquidity(df)
    df = remove_financial_sectors(df)
    df = order_by_ev_ebitda(df)
    df = add_ticker_base_column(df)
    df = remove_duplicate_ticker_base(df)
    log_warnings()
    save_file()
    return df