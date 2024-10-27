# Custom mapping function for Hebrew alphabet characters
from pyluach.dates import HebrewDate

from custom_logger import logger


# Custom mapping function for Hebrew alphabet characters
def gematria(hebrew_string):
    hebrew_numeric_map = {
        'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
        'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40, 'נ': 50, 'ן': 50,
        'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80, 'צ': 90, 'ץ': 90, 'ק': 100, 'ר': 200,
        'ש': 300, 'ת': 400,
        '"': 0, "'": 0, "`": 0, "״": 0
    }
    return sum(hebrew_numeric_map[ch] for ch in hebrew_string)


# Custom mapping for Hebrew month names
hebrew_month_map = {
    'ניסן': 1, 'אייר': 2, 'סיוון': 3, 'תמוז': 4, 'אב': 5, 'אלול': 6,
    'תשרי': 7, 'חשוון': 8, 'כסלו': 9, 'טבת': 10, 'שבט': 11, 'אדר': 12,
    'אדר א': 12, 'אדר ב': 13
}


def heb_date_str_to_hebrew_date(date_str: str) -> HebrewDate:
    date_parts = date_str.split()
    if not date_parts:
        raise ValueError()

    if (len(date_parts) > 2) and gematria(date_parts[-1]) > 2:
        year_letters = date_parts.pop().replace("הת", "ת")
    else:
        year_letters = HebrewDate.today().hebrew_year(thousands=False)

    month_candidate = date_parts.pop()
    month_name = month_candidate if len(date_parts) == 1 else f"{date_parts.pop()} {month_candidate}"
    day_letters = date_parts.pop()

    day = gematria(day_letters)
    month = hebrew_month_map[month_name]
    year = gematria(year_letters) + 5000

    return HebrewDate(year, month, day)


def date_parts_to_date(day, month, year=None):
    heb_year = year or HebrewDate.today().year
    logger.info(f"converting date parts to hebrew date: year={year}, month={month}, day={day}")
    return HebrewDate(heb_year, month, day)
