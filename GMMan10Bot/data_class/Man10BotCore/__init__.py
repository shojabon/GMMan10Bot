from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from GMMan10Bot import GMMan10Bot


class Man10BotCore:

    def __init__(self, main: GMMan10Bot):
        self.main = main

    def get_system_prompt(self, question: str, user_info: dict = None) -> str:
        return ""

    def get_chat_history_prompt(self, question: str, user_info: dict = None) -> list[dict]:
        return []

    def generate_response(self, question: str, user_info: dict = None) -> str:
        return ""

    def get_path(self, file_name: str = None):
        relative_path = "config/cores/"
        # return absolute path
        import os
        absolute_path = os.path.abspath(relative_path)
        if file_name is None:
            return absolute_path
        # separate file with file separator
        return absolute_path + os.sep + file_name
