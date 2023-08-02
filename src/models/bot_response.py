from typing import List, Any


class BotResponse:
    def __init__(self, text):
        self.text = text
        self.items_display = None
        self.items_callback_data = None
        self.action = None

    def add_inline_items(self, items_display: List[str], items_callback_data: List[Any], action: str = None):
        if len(items_display) != len(items_callback_data):
            raise ValueError("items_display and items_callback_data are not at the same length")

        self.action = action
        self.items_display = items_display
        self.items_callback_data = items_callback_data
