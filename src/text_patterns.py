from date_utils import heb_date_str_to_hebrew_date


def is_start_msg(text):
    return text == 'start'


def is_date_msg(text):
    try:
        heb_date_str_to_hebrew_date(text)
        return True
    except Exception as e:
        return False
