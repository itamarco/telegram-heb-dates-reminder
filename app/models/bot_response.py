from dataclasses import dataclass


@dataclass
class BotResponse:
    text: str
    inline_buttons: list[tuple[str, str]] = None
