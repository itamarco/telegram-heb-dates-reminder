from datetime import date
import unittest
from unittest.mock import patch

from user_flow import calc_next_reminder_date


class AppFlowTest(unittest.TestCase):
    @patch('datetime.date')
    def test_next_reminder_future_date(self, mock_date):
        mock_date.today.return_value = date(2023, 7, 18)
        test_cases = [
            ((5990, 4, 25), 7, date(2230, 6, 30)),
            ((5754, 11, 25), 4, date(2024, 1, 31)),
            ((None, 11, 25), 4, date(2024, 1, 31)),
            ((5750, 5, 9), 1, date(2023, 7, 26))
        ]

        for heb_date_input, reminder_days, reminder_date in test_cases:
            with self.subTest():  # heb_date=heb_date_input, reminder_days=reminder_days, expected=reminder_date):
                next_reminder = calc_next_reminder_date(heb_date_input, reminder_days)
                self.assertEqual(reminder_date, next_reminder,
                                 msg=f"Bad response for input {heb_date_input, reminder_days}")

        # next_reminder = calc_next_reminder_date((5990, 4, 25), reminder_days=7)
        # self.assertEqual(next_reminder, date(2299, 12, 1))  # add assertion here


if __name__ == '__main__':
    unittest.main()
