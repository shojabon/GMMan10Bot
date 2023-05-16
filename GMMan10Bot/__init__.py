import json

from GMMan10Bot.cores.QABasicCore import QABasicCore
from GMMan10Bot.extentions.Man10BotEmbeddings import Man10BotEmbeddings
from GMMan10Bot.extentions.Man10BotSearch import Man10BotSearch
from GMMan10Bot.applications.Man10BaseKnowledge import Man10BaseKnowledge
from GMMan10Bot.data_class.Man10BotApplication import Man10BotApplication
import openai
from pymongo import MongoClient


class GMMan10Bot:

    def __init__(self):
        # load config
        with open("config/config.json", "r", encoding="utf-8") as f:
            self.config = json.loads(f.read())

        openai.api_key = self.config["openaiKey"]
        # load mongodb
        self.mongo = MongoClient(self.config["mongodb"])

        # load embeddings
        self.embeddings = Man10BotEmbeddings(self)
        # load search
        self.search = Man10BotSearch(self)

        self.applications: dict[str, Man10BotApplication] = {}

        # load applications
        self.register_application(Man10BaseKnowledge(self))


        # load search vectors

        self.search.load_search_vector_to_map()

        self.core = QABasicCore(self)

        print(self.core.generate_response("まんぼ、ギャンブラーランクになる方法は？"))


    def register_application(self, application: Man10BotApplication):
        application_path = application.get_path()
        # generate directories if not exists
        import os
        if not os.path.exists(application_path):
            os.makedirs(application_path)

        self.applications[application.name] = application
        self.applications[application.name].on_load()

    def get_knowledge_dictionary(self):
        result = {}
        for application in self.applications.values():
            result.update(application.knowledge)
        return result
