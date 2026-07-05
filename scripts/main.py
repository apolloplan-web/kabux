import os
import json
import gspread
from google.oauth2.service_account import Credentials
import yfinance as yf
from datetime import datetime

# 定義2, 6: 東証証券コードをハードコード（最大40件）
# ※ ユーザーの要望である「6230」を初期値として設定。必要に応じて最大40件まで追加可能。
TICKERS = [
    "2148.T",#  01 アイティメディア
    "7023.T",# ユーザー指定の銘柄 02 東京ラヂエーター製造
    "4923.T",# ユーザー指定の銘柄 03 コタ
    "9432.T",# ユーザー指定の銘柄 04 日本電信電話（NTT）
    "9904.T",# ユーザー指定の銘柄 05 ベリテ
    "9997.T",# ユーザー指定の銘柄 06 ベルーナ
    "6539.T",# ユーザー指定の銘柄 07 MS-Japan
    "3465.T",# ユーザー指定の銘柄 08 ケイアイスター不動産
    "6523.T",# ユーザー指定の銘柄 09 PHCホールディングス
    "7414.T",# ユーザー指定の銘柄 10 小野建
    "7638.T",# ユーザー指定の銘柄 11 NEW ART HOLDINGS
    "7203.T",# ユーザー指定の銘柄 12 トヨタ自動車
    "1898.T",# ユーザー指定の銘柄 13 世紀東急工業
    "3131.T",# ユーザー指定の銘柄 14 シンデン・ハイテックス
    "1820.T",# ユーザー指定の銘柄 15 西松建設
    "3284.T",# ユーザー指定の銘柄 16 フージャースホールディングス
    "6419.T",# ユーザー指定の銘柄 17 マースグループホールディングス
    "4671.T",# ユーザー指定の銘柄 18 ファルコホールディングス
    "3548.T",# ユーザー指定の銘柄 19 バロックジャパンリミテッド
    "8897.T" # ユーザー指定の銘柄 20 MIRARTHホールディングス
    # "7203.T",  # 必要に応じてここに追記していく
]

def main():
    # 1. GitHub SecretsからGoogleサービスアカウントの鍵を取得
    secret_key = os.environ.get("GOOGLE_SERVICE_ACCOUNT_KEY")
    if not secret_key:
        print("Error: GOOGLE_SERVICE_ACCOUNT_KEY is not set in environment variables.")
        return

    # APIスコープの定義
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    try:
        # JSON文字列をディクショナリに変換して認証
        creds_dict = json.loads(secret_key)
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        gc = gspread.authorize(creds)
        
        # 定義4: スプレッドシートIDとシート名「シート2」を指定して開く
        SPREADSHEET_ID = "1BCdhR7EjPR3xlxwEd1NF2jucQGn3UMqxQhEPSDo7Cog"
        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.worksheet("シート2")
    except Exception as e:
        print(f"Google APIの認証またはスプレッドシートの接続に失敗しました: {e}")
        return

    rows_to_append = []

    # 2. 各銘柄の情報取得ループ
    for ticker_code in TICKERS:
        code_str = ticker_code.replace(".T", "") # 表示用に「.T」を除く
        name = "N/A"
        date_str = datetime.now().strftime("%Y-%m-%d")
        price = "N/A"
        
        try:
            ticker = yf.Ticker(ticker_code)
            
            # 銘柄名の取得を試みる
            try:
                name = ticker.info.get('longName') or ticker.info.get('shortName') or code_str
            except:
                name = code_str
            
            # 終値と日付の取得（直近の履歴データから取得するのが最も確実）
            hist = ticker.history(period="2d")
            if not hist.empty:
                latest_row = hist.iloc[-1]
                price = float(latest_row['Close'])
                date_str = latest_row.name.strftime("%Y-%m-%d")
            else:
                raise ValueError("yfinanceから履歴データを取得できませんでした。")
                
            # 定義5: 証券コード、銘柄名、終値日付、終値
            rows_to_append.append([code_str, name, date_str, price])
            print(f"Success: {code_str} - {price}円")

        except Exception as e:
            # 定義7: 終値が取得できない場合はエラーメッセージを記録する
            error_msg = f"エラー: {str(e)}"
            rows_to_append.append([code_str, name, date_str, error_msg])
            print(f"Failed: {code_str} - {error_msg}")

    # 3. スプレッドシートへ一括追記（パターンA：追記型）
    if rows_to_append:
        try:
            worksheet.append_rows(rows_to_append, value_input_option='USER_ENTERED')
            print(f"スプレッドシートに {len(rows_to_append)} 件のデータを追記しました。")
        except Exception as e:
            print(f"スプレッドシートへの書き込みに失敗しました: {e}")

if __name__ == "__main__":
    main()
