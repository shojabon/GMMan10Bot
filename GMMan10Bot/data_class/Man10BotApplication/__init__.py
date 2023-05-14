from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from GMMan10Bot import GMMan10Bot
    from GMMan10Bot.data_class.Man10BotKnowledge import Man10BotKnowledge


class Man10BotApplication:

    def __init__(self, main: GMMan10Bot):
        self.main = main
        self.knowledge = {}

    def register_knowledge(self, knowledge: Man10BotKnowledge):
        knowledge.application = knowledge
        self.knowledge[knowledge.id] = knowledge
