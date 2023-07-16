# Initialize the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.reminder import Base, ReminderDAO

engine = create_engine('sqlite:///reminders.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

reminderDao = ReminderDAO(Session())
