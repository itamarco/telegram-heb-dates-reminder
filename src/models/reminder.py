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
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def create(self, reminder):
        with self.Session() as session:
            session.add(reminder)
            session.commit()
            session.refresh(reminder)
        return reminder

    def read(self, id):
        with self.Session() as session:
            return session.query(Reminder).filter_by(id=id).first()

    def update(self, reminder):
        with self.Session() as session:
            session.merge(reminder)
            session.commit()

    def update_all(self, reminders):
        session = self.Session()
        for reminder in reminders:
            session.merge(reminder)
        session.commit()

    def delete(self, reminder):
        session = self.Session()
        session.delete(reminder)
        session.commit()

    def find_by_user(self, userId):
        session = self.Session()
        return session.query(Reminder).filter_by(userId=userId).all()

    def find_by_date(self, date) -> List[Reminder]:
        session = self.Session()
        return session.query(Reminder).filter_by(nextReminder=date).all()

    def delete_by_userid_description(self, user_id, description) -> int:
        session = self.Session()
        try:
            reminders = session.query(Reminder) \
                .filter(Reminder.userId == user_id, Reminder.description == description) \
                .all()
            for reminder in reminders:
                session.delete(reminder)
            session.commit()
            return len(reminders)
        except NoResultFound:
            return 0
