from __future__ import annotations

import traceback
from typing import TYPE_CHECKING

import numpy as np
import openai
from cleantext import clean

if TYPE_CHECKING:
    from GMMan10Bot import GMMan10Bot


class Man10BotEmbeddings:

    def __init__(self, main: GMMan10Bot):
        self.main = main

        self.memory_cache = {}

    def get_ada_embedding_of_text(self, text: str):
        result = self.get_ada_embedding_of_text_batch([text])
        if len(result) == 0:
            return None
        return result[text]

    def get_ada_embedding_of_text_batch(self, text: list[str] | str):
        if type(text) == str:
            text = [text]
        # delete all ''
        text = [x for x in text if x != '']
        if len(text) == 0:
            return {}

        result = {}
        for single_text in text:
            result[single_text] = None

        try:
            # check cache
            for idx, single_text in enumerate(text):
                if single_text in self.memory_cache:
                    result[single_text] = self.memory_cache[single_text]

            cache = self.main.mongo["man10bot"]["ada_embedding_cache"].find({"text": {"$in": [x for x in text if result[x] is None]}})
            for cache_data in cache:
                result[cache_data["text"]] = cache_data["embedding"]
                self.memory_cache[cache_data["text"]] = cache_data["embedding"]

            text = [x for x in text if result[x] is None]
            remaining_result = {}
            if len(text) == 0:
                return result
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )
            for idx, single_remaining_text in enumerate(text):
                remaining_result[single_remaining_text] = response["data"][idx]

            # insert into cache
            insert_data = []
            for single_remaining_text in text:
                insert_data.append({"text": single_remaining_text, **remaining_result[single_remaining_text]})
            self.main.mongo["man10bot"]["ada_embedding_cache"].insert_many(insert_data)
            cache = self.main.mongo["man10bot"]["ada_embedding_cache"].find({"text": {"$in": text}})
            for cache_data in cache:
                result[cache_data["text"]] = cache_data["embedding"]
                self.memory_cache[cache_data["text"]] = cache_data["embedding"]
            return result
        except Exception:
            traceback.print_exc()
            print(text)
            return result

    def get_most_similar(self, text: str, data: list[str]):
        # remove all "" from data
        data = [x for x in data if x != '']
        text_vector = self.get_ada_embedding_of_text(text)
        if text_vector is None:
            return None
        data_embeddings = self.get_ada_embedding_of_text_batch(data)
        if len(data_embeddings) == 0:
            return None

        data_vectors = []
        for data_text in data:
            data_vectors.append(data_embeddings[data_text])
        text_vector, data_vector = np.array(text_vector), np.array(data_vectors)

        result = np.dot(data_vector, text_vector)
        result = np.argsort(result)[::-1]

        # return the most similar text
        return data[result[0]]