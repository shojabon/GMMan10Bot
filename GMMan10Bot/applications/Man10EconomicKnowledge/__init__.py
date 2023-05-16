from __future__ import annotations

import csv
import datetime
import json
import uuid
from typing import TYPE_CHECKING

from oauth2client.service_account import ServiceAccountCredentials
import gspread

from GMMan10Bot.data_class.Man10BotKnowledge import Man10BotKnowledge
from GMMan10Bot.data_class.Man10BotKnowledgeData import ConversationalKnowledge

if TYPE_CHECKING:
    from GMMan10Bot import GMMan10Bot
from GMMan10Bot.data_class.Man10BotApplication import Man10BotApplication


class Man10EconomicKnowledge(Man10BotApplication):

    def __init__(self, main: GMMan10Bot):
        super().__init__(main)
        self.name = "Man10EconomicKnowledge"
        self.data = {}

    def on_load(self):

        # open json file
        with open(self.get_path('user_balance.json'), 'r') as f:
            self.data = json.loads(f.read())["rows"]

        for user in self.data[:1000]:
            knowledge = Man10BotKnowledge()
            def get_balance(username: str, balance: int):
                data = ConversationalKnowledge()
                data.question = username + "はお金をいくら持ってますか？"
                data.answer = str(balance) + "円持っています。"
                return data

            knowledge.get_data = get_balance
            player = user["player"]
            knowledge.anchor_questions = [player + "の所持金を教えて",
                                          player + "はいくら持ってる？",
                                          player + "の電子マネーはいくら？",
                                          player + "のお金はどれぐらいある？"
                                          ]
            knowledge.execution_args = {"username": player, "balance": user["total"]}
            self.register_knowledge(knowledge)
        print(len(self.knowledge), "aaaa")
