import unittest

from date_utils import heb_date_str_to_hebrew_date


class HebrewDateFromString(unittest.TestCase):
    def test_valid_inputs(self):
        test_cases = [
            ("כה שבט תשנד", (5754, 11, 25)),
            ("א אב", (5783, 5, 1)),
            ("כג אדר א תשסא", (5761, 12, 23)),
            ("יב אדר ב תשסג", (5763, 13, 12)),
            ("כג אדר א", (5783, 12, 23))
        ]

        for input, expected in test_cases:
            with self.subTest(input=input, expected=expected):
                hebrew_date = heb_date_str_to_hebrew_date(input)
                print(hebrew_date.hebrew_date_string())
                result = hebrew_date.tuple()
                self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
