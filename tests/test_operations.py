import unittest
from datetime import date

from models.reminder import Reminder
from operations import pretty_print_reminder


class OperationsTest(unittest.TestCase):
    def test_pretty_print_reminder(self):
        reminder = Reminder(
            id=220,
            userId=34329988,
            description="יום הולדת למעיין!",
            eventDay=9,
            eventMonth=1,
            eventYear=5780,
            reminderDays=31,
            nextReminder=date(2024, 3, 19),
            repeat=True
        )
        print(pretty_print_reminder(reminder))


if __name__ == '__main__':
    unittest.main()
