import datetime
from unittest import TestCase
from unittest.mock import patch

from pyluach.dates import HebrewDate


class PyluachTest(TestCase):
    @patch('datetime.datetime.today', return_value=datetime.datetime(1984, 1, 29, 10, 0, 0))
    def test_comparison(self, mock_today):
        print(HebrewDate.today().hebrew_date_string())
