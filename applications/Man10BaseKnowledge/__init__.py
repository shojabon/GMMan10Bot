from __future__ import annotations

import csv
import uuid
from typing import TYPE_CHECKING

from oauth2client.service_account import ServiceAccountCredentials
import gspread

from GMMan10Bot.data_class.Man10BotKnowledge import Man10BotKnowledge
from GMMan10Bot.data_class.Man10BotKnowledgeData import ConversationalKnowledge

if TYPE_CHECKING:
    from GMMan10Bot import GMMan10Bot
from GMMan10Bot.data_class.Man10BotApplication import Man10BotApplication


class Man10BaseKnowledge(Man10BotApplication):

    def __init__(self, main: GMMan10Bot):
        super().__init__(main)
        self.name = "Man10BaseKnowledge"

    def on_load(self):
        # self.download_spread_sheet()
        self.load_csv()

    def download_spread_sheet(self):
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

    def load_csv(self):
        file = open(self.get_path("qadata.csv"), "r", encoding="utf-8")
        reader = csv.reader(file)
        for row in [x for x in reader][1:]:
            linked_id = str(uuid.uuid4())

            def get_data(knowledge_object: Man10BotKnowledge, answer: str):
                data = ConversationalKnowledge()
                data.question = knowledge_object.anchor_questions
                data.answer = answer
                return data
            for question in row[2].split("\n"):
                knowledge = Man10BotKnowledge()
                knowledge.linked_id = linked_id
                knowledge.anchor_questions = question
                knowledge.anchor_keywords = row[1].split("\n")
                knowledge.execution_args = {"answer": row[3]}
                knowledge.get_data = get_data

                self.register_knowledge(knowledge)

        file.close()
