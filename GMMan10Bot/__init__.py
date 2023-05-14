import json

from GMMan10Bot.data_class.Man10BotApplication import Man10BotApplication


class GMMan10Bot:

    def __init__(self):
        # load config
        with open("config.json", "r", encoding="utf-8") as f:
            self.config = json.loads(f.read())

        self.applications = {}

    def register_application(self, application: Man10BotApplication):
        self.applications[application.name] = application