from datetime import datetime, timedelta

def verify_file_data(start_date, end_date, history):
    latest_date_str = history.iloc[-1].Date
    latest_date = datetime.strptime(latest_date_str, '%Y-%m-%d')

    difference = (end_date - latest_date).days 
    outdated_file = difference > 3

    if(outdated_file):
        start_date = latest_date + timedelta(days=1)

    return outdated_file, start_date


def build_file_name(asset, sufix):
    return f"csv_files/{asset.lower()}_{sufix}.csv"