from __future__ import annotations

import traceback
from typing import TYPE_CHECKING

import numpy as np
import openai
from cleantext import clean

from GMMan10Bot.data_class.Man10BotKnowledge import Man10BotKnowledge

if TYPE_CHECKING:
    from GMMan10Bot import GMMan10Bot


class Man10BotSearch:

    def __init__(self, main: GMMan10Bot):
        self.main = main
        self.knowledge_vector, self.knowledge_ids = [], []

    def load_search_vector_to_map(self):
        all_knowledge = self.main.get_knowledge_dictionary()
        for knowledge in all_knowledge.values():
            for question in knowledge.anchor_questions:
                vector = self.main.embeddings.get_ada_embedding_of_text(question)
                if vector is None:
                    continue
                self.knowledge_vector.append(vector)
                self.knowledge_ids.append(knowledge.unique_id)

        self.knowledge_vector, self.knowledge_ids = np.array(self.knowledge_vector), np.array(self.knowledge_ids)

    def search_knowledge(self, question: str) -> list[Man10BotKnowledge]:
        all_knowledge = self.main.get_knowledge_dictionary()

        question_vector = self.main.embeddings.get_ada_embedding_of_text(question)
        result = np.dot(self.knowledge_vector, question_vector)
        result = np.argsort(result)[::-1]

        # return sorted knowledge objects
        return [all_knowledge[self.knowledge_ids[x]] for x in result]
