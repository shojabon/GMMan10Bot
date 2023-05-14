from __future__ import annotations

from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from GMMan10Bot.data_class.Man10BotApplication import Man10BotApplication


class Man10BotKnowledge:

    def __init__(self):
        self.id = self.generate_id()
        self.application: Man10BotApplication | None = None

    def generate_id(self):
        return str(uuid.uuid4())
