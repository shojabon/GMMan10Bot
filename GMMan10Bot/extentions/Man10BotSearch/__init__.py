from __future__ import annotations

import traceback
from typing import TYPE_CHECKING

import numpy as np
import openai
from cleantext import clean
from tqdm import tqdm

from GMMan10Bot.data_class.Man10BotKnowledge import Man10BotKnowledge

if TYPE_CHECKING:
    from GMMan10Bot import GMMan10Bot


class Man10BotSearch:

    def __init__(self, main: GMMan10Bot):
        self.main = main
        self.knowledge_vector, self.knowledge_ids = [], []

    def load_search_vector_to_map(self):
        all_questions = []
        all_knowledge = self.main.get_knowledge_dictionary()

        for knowledge in all_knowledge.values():
            for question in knowledge.anchor_questions:
                all_questions.append(question)


        all_text_vectors = {}
        # break into batches of 100
        all_questions = [all_questions[i:i + 100] for i in range(0, len(all_questions), 100)]
        for batch in tqdm(all_questions):
            result = self.main.embeddings.get_ada_embedding_of_text_batch(batch)
            for text in result:
                all_text_vectors[text] = result[text]

        for knowledge in all_knowledge.values():
            for question in knowledge.anchor_questions:
                if question == "":
                    continue
                self.knowledge_vector.append(all_text_vectors[question])
                self.knowledge_ids.append(knowledge.unique_id)

        self.knowledge_vector, self.knowledge_ids = np.array(self.knowledge_vector), np.array(self.knowledge_ids)

    def search_knowledge(self, question: str) -> list[Man10BotKnowledge]:
        all_knowledge = self.main.get_knowledge_dictionary()

        question_vector = self.main.embeddings.get_ada_embedding_of_text(question)
        result = np.dot(self.knowledge_vector, question_vector)
        result = np.argsort(result)[::-1]

        # return sorted knowledge objects
        return [all_knowledge[self.knowledge_ids[x]] for x in result]
