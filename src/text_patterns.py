from date_utils import heb_date_str_to_hebrew_date, gematria


def is_start_msg(text):
    return text == 'start'


def is_date_msg(text):
    try:
        heb_date_str_to_hebrew_date(text)
        return True
    except Exception as e:
        return False


def date_string_has_year(text):
    date_parts = text.split()
    return len(date_parts) > 2 and gematria(date_parts[-1]) > 2
