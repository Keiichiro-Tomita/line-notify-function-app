from datetime import datetime, timedelta, timezone
import pandas as pd
import re
import os
import logging
import azure.functions as func
from line_notify import send_line_notify  # 修正後の関数をインポート

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.now(timezone.utc).isoformat()  # UTC時間を取得
    logging.info(f"Python timer trigger function ran at {utc_timestamp}")

    file_path = os.getenv('FILE_PATH', r"C:\Users\keiichiro-tomita\Downloads\カレンダー.xlsx")  # 例のパスを環境変数から取得
    
    try:
        df = pd.read_excel(file_path, sheet_name=0, skiprows=1)  # Excel読み込み
    except FileNotFoundError:
        logging.error(f"ファイルが見つかりません: {file_path}")
        return

    df.columns = df.columns.str.strip()

    start_date_col = '開始日'

    df[start_date_col] = df[start_date_col].astype(str).str.strip()
    df[start_date_col] = df[start_date_col].apply(lambda x: re.sub(r'\s*\(.*\)', '', x))  # 曜日削除

    df[start_date_col] = df[start_date_col].str.replace(r'年', '-', regex=True)
    df[start_date_col] = df[start_date_col].str.replace(r'月', '-', regex=True)
    df[start_date_col] = df[start_date_col].str.replace(r'日', '', regex=True)

    df[start_date_col] = pd.to_datetime(df[start_date_col], errors='coerce')

    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
    tomorrow_date = tomorrow.strftime('%Y-%m-%d')

    if tomorrow_date in df[start_date_col].dt.strftime('%Y-%m-%d').values:
        tomorrow_row = df[df[start_date_col].dt.strftime('%Y-%m-%d') == tomorrow_date]
        tomorrow_date = tomorrow_row.iloc[0]['開始日']
        formatted_tomorrow_date = f"{tomorrow_date.month}/{tomorrow_date.day}"
        担当者 = tomorrow_row.iloc[0]['タイトル']
        
        message = f"【子供たちの登校を見守る当番】\nお疲れ様です。\n明日{formatted_tomorrow_date}は【{担当者}さん】の当番となっています！\nよろしくお願いします。"
        logging.info(message)
        send_line_notify(message)  # LINE通知を送る
    else:
        logging.info("明日は当番なし！")
