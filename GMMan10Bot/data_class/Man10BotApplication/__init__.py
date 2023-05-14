from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from GMMan10Bot import GMMan10Bot
    from GMMan10Bot.data_class.Man10BotKnowledge import Man10BotKnowledge


class Man10BotApplication:

    def __init__(self, main: GMMan10Bot):
        self.main = main
        self.knowledge = {}
        self.name = None

    def register_knowledge(self, knowledge: Man10BotKnowledge):
        knowledge.application = knowledge
        self.knowledge[knowledge.id] = knowledge

    def get_path(self, file_name: str = None):
        relative_path = "config/application/" + str(self.name)
        # return absolute path
        import os
        absolute_path = os.path.abspath(relative_path)
        if file_name is None:
            return absolute_path
        # separate file with file separator
        return absolute_path + os.sep + file_name
    def on_load(self):
        pass