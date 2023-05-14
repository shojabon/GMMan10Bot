from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from GMMan10Bot.data_class.Man10BotApplication import Man10BotApplication


class Man10BotKnowledge:

    def __init__(self):
        self.id = self.generate_id()
        self.application: Man10BotApplication | None = None
        self.anchor_questions = []
        self.anchor_keywords = []
        self.data_title = ""

    def is_allowed_to_use(self, user_info, message, search_metadata) -> bool:
        return True
    def get_data(self, user_info, message, search_metadata) -> str:
        pass
    def generate_id(self):
        return str(uuid.uuid4())
