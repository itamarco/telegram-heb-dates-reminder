from enum import Enum


class TEXTS(str, Enum):
    CLICK_EVENT_TO_DELETE = "לחץ על אירוע שברצונך למחוק"
    INSTRUCTIONS = 'כדי להכניס אירוע חדש, התחל בשליחה של התאריך העברי שלו (לדוגמא: "כה שבט תשנד" / "יב אב"). אם התאריך תקין הבוט ידריך אותך איך להמשיך'
    SET_DESCRIPTION = "כותרת לאירוע:",
    SET_REMINDER_DAYS = "כמה ימים מראש להתריע?",
    REMINDER_ADDED = "תזכורת התווספה בהצלחה! 👍🏼",
    WELCOME = "ברוך הבא! בחר באופציה המתאימה"
    FLOW_ERROR = "סליחה אני לא מבין את הבקשה 😥"


class TEXT_FORMATS(str, Enum):
    EVENT_DELETED = "האירוע '{title}' נמחק בהצלחה"
    EVENT_IS_COMING = "בעוד {days} ימים: {event} 🔔"
    EVENT_PRETTY_PRINT = "📅 {title}, \t{date}\t[{reminder_days_list}]"
    REMINDER_PRETTY_PRINT = "({id}): {title},\t{date}\t🕙{reminder_days}\t 📅\t{next_reminder}"


class OP(str, Enum):
    INSTRUCTIONS = "הוראות"
    LIST_EVENTS = "רשימת אירועים"
    LIST_REMINDERS = "רשימת תזכורות"
    DELETE_EVENT = "מחק אירוע"
    TODAY = "היום"


class CALLBACK_ACTION(str, Enum):
    DELETE = "delete"
