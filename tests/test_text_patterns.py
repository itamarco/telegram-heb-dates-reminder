import unittest

from text_patterns import is_date_msg


class MessagePatterns(unittest.TestCase):
    def test_is_date_msg(self):
        test_cases = [
            ("כה שבט תשנד", True),
            ("א אב", True),
            ("כג אדר א תשסא", True),
            ("כג אדר א", True),

            ("אב לא הולך", False),
            ("סתם טקסט", False),
            ("", False),
        ]

        for input, expected in test_cases:
            with self.subTest(input=input, expected=expected):
                result = is_date_msg(input)
                self.assertEqual(expected, result, msg=f"Bad response for input {input}")


if __name__ == '__main__':
    unittest.main()
