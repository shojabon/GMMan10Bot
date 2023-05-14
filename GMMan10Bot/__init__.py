import json


class GMMan10Bot:

    def __init__(self):
        # load config
        with open("config.json", "r", encoding="utf-8") as f:
            self.config = json.loads(f.read())
        