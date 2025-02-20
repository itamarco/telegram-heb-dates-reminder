# Initialize the database
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.reminder import Base, ReminderDAO

POSTGRES_URL = os.environ.get("POSTGRES_DATABASE_URL_UNPOOLED")
engine = create_engine(POSTGRES_URL)  # ('sqlite:///reminders.db')
Base.metadata.create_all(engine)

reminder_dao = ReminderDAO(engine)
