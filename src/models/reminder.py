import collections
from email.policy import default
from typing import List

from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Initialize the database
engine = create_engine('sqlite:///reminders.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()


# Define the Reminder model
class Reminder(Base):
    __tablename__ = 'reminder'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer)
    description = Column(String)
    eventDay = Column(Integer)
    eventMonth = Column(Integer)
    eventYear = Column(Integer)
    reminderDays = Column(Integer)
    nextReminder = Column(Date)
    lastReminder = Column(Date, default=None)
    repeat = Column(Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.userId,
            'reminder_days': self.reminderDays,
            'heb_date': f"{self.eventDay}-{self.eventMonth}-{self.eventYear}",
            'description': self.description,
            'next_reminder': f"{self.nextReminder.day}/{self.nextReminder.month}/{self.nextReminder.year}",
        }

    def __repr__(self):
        return f"<Reminder(id={self.id}, userId={self.userId}, description='{self.description}', \
                eventDay={self.eventDay}, eventMonth={self.eventMonth}, eventYear={self.eventYear}, \
                reminderDays={self.reminderDays}, nextReminder='{self.nextReminder}')>"


# Define the Reminder DAO class
class ReminderDAO:
    def __init__(self, session):
        self.session = session

    def create(self, reminder):
        self.session.add(reminder)
        self.session.commit()

    def read(self, id):
        return self.session.query(Reminder).filter_by(id=id).first()

    def update(self, reminder):
        self.session.merge(reminder)
        self.session.commit()

    def update_all(self, reminders):
        for reminder in reminders:
            self.session.merge(reminder)
        self.session.commit()

    def delete(self, reminder):
        self.session.delete(reminder)
        self.session.commit()

    def find_by_user(self, userId):
        return self.session.query(Reminder).filter_by(userId=userId).all()

    def find_by_date(self, date) -> List[Reminder]:
        return self.session.query(Reminder).filter_by(nextReminder=date).all()

    def delete_by_userid_description(self, user_id, description) -> int:
        try:
            reminders = self.session.query(Reminder) \
                .filter(Reminder.userId == user_id, Reminder.description == description) \
                .all()
            for reminder in reminders:
                self.session.delete(reminder)
            self.session.commit()
            return len(reminders)
        except NoResultFound:
            return 0
