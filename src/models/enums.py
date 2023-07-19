from enum import Enum


class TEXTS(str, Enum):
    SET_DESCRIPTION = "תיאור קצר של האירוע:",
    SET_REMINDER_DAYS = "כמה ימים מראש להתריע?",
    REMINDER_ADDED = "תזכורת התווספה בהצלחה",
    FLOW_ERROR = "Internal flow error"


class OP(str, Enum):
    LIST_EVENTS = "רשימת תזכורות",
    DELETE_EVENT = "מחק תזכורת",
