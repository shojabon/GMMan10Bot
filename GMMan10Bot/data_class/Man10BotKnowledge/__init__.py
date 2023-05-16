from __future__ import annotations

import inspect
from enum import Enum
from typing import TYPE_CHECKING
import uuid

from GMMan10Bot.data_class.Man10BotKnowledgeData import MetaKnowledge, ConversationalKnowledge

if TYPE_CHECKING:
    from GMMan10Bot.data_class.Man10BotApplication import Man10BotApplication


class Man10BotKnowledge:

    def __init__(self):
        self.unique_id = self.generate_id()
        self.linked_id = None
        self.application: Man10BotApplication | None = None
        self.anchor_questions = []
        self.anchor_keywords = []
        self.execution_args = {}

    def is_allowed_to_use(self, question, user_info, search_metadata) -> bool:
        return True

    def get_data(self) -> ConversationalKnowledge | MetaKnowledge:
        pass

    def execute_get_data(self, question=None, user_info=None, search_metadata=None, **kwargs):
        params = {"knowledge_object": self, "user_info": user_info, "question": question,
                  "search_metadata": search_metadata}
        # extend kwargs
        params.update(kwargs)
        params.update(self.execution_args)
        function = self.get_data
        # adjust params so that it matches the function's signature
        function_args = inspect.signature(function).parameters.keys()
        function_args = list(function_args)
        # if params doesn't have a function arg, add it with None
        for arg in function_args:
            if arg not in params:
                params[arg] = None

        # if params has an arg that the function doesn't have, remove it
        for arg in list(params.keys()):
            if arg not in function_args:
                del params[arg]
        return self.get_data(**params)

    def generate_id(self):
        return str(uuid.uuid4())
