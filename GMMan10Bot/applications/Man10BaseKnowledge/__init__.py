from __future__ import annotations

import csv
from typing import TYPE_CHECKING

from oauth2client.service_account import ServiceAccountCredentials
import gspread

if TYPE_CHECKING:
    from GMMan10Bot import GMMan10Bot
from GMMan10Bot.data_class.Man10BotApplication import Man10BotApplication


class Man10BaseKnowledge(Man10BotApplication):

    def __init__(self, main: GMMan10Bot):
        super().__init__(main)
        self.name = "Man10BaseKnowledge"

    def on_load(self):
        self.load_spread_sheet()
    def load_spread_sheet(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.get_path("key.json"), scope)
        client = gspread.authorize(creds)

        # スプレッドシートを開く
        spreadsheet = client.open('man10_qa')
        worksheet = spreadsheet.worksheet('Q&A')

        # シートのデータを取得
        data = worksheet.get_all_values()

        # CSVファイルに出力
        with open(self.get_path("qadata.csv"), 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
