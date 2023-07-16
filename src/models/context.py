from typing import Tuple

# (year = None, month, day)
DateTuple = Tuple[int | None, int, int]


class Context:
    def __init__(self, user_id):
        self.user_id = user_id

    last_stage = None
    heb_date_tuple: DateTuple = None
    description = None
