import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stocks import stock_history

def classify(correlation):
    if correlation <= -0.7:
        return "Forte correlação negativa"
    elif -0.7 < correlation <= -0.3:
        return "Fraca correlação negativa"
    elif -0.3 < correlation < 0.3:
        return "Não correlacionado"
    elif 0.3 <= correlation < 0.7:
        return "Fraca correlação positiva"
    else:
        return "Forte correlação positiva"
    

def calculate(asset1, asset2):
    history1 = stock_history.get_history(asset1)
    history2 = stock_history.get_history(asset2)

    close1 = history1[['Date', 'Close']].rename(columns={'Close': f'Close_{asset1}'})
    close2 = history2[['Date', 'Close']].rename(columns={'Close': f'Close_{asset2}'})

    combined_data = pd.merge(close1, close2, on='Date')
    correlation = combined_data[f'Close_{asset1}'].corr(combined_data[f'Close_{asset2}'])
    correlation = float(round(correlation, 2))

    classification = classify(correlation)
    return {'correlation':  correlation, 'result': classification}

def calculate_for_wallet(wallet, stocks_under_evaluation):
    results = []

    for stock_wallet in wallet:
        for stock_eval in stocks_under_evaluation:
            corr_value = calculate(stock_wallet, stock_eval)
            results.append({
                'Stock_Wallet': stock_wallet,
                'Stock_Eval': stock_eval,
                'Correlation': corr_value['correlation'],
                'Result': corr_value['result']
            })

    return pd.DataFrame(results)