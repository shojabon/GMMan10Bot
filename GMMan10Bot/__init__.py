import json

from applications.Man10BaseKnowledge import Man10BaseKnowledge
from GMMan10Bot.data_class.Man10BotApplication import Man10BotApplication


class GMMan10Bot:

    def __init__(self):
        # load config
        with open("config/config.json", "r", encoding="utf-8") as f:
            self.config = json.loads(f.read())

        self.applications: dict[str, Man10BotApplication] = {}

        # load applications
        self.register_application(Man10BaseKnowledge(self))

    def register_application(self, application: Man10BotApplication):
        application_path = application.get_path()
        # generate directories if not exists
        import os
        if not os.path.exists(application_path):
            os.makedirs(application_path)

        self.applications[application.name] = application
        self.applications[application.name].on_load()