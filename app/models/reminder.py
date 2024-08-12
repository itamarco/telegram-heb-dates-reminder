from typing import List

from sqlalchemy import Column, Integer, String, Date, Boolean, text
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Define the Reminder model
class Reminder(Base):
    __tablename__ = 'reminder'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    description = Column(String)
    event_day = Column(Integer)
    event_month = Column(Integer)
    event_year = Column(Integer)
    reminder_days = Column(Integer)
    next_reminder = Column(Date)
    last_reminder = Column(Date, default=None)
    repeat = Column(Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'reminder_days': self.reminder_days,
            'heb_date': f"{self.event_day}-{self.event_month}-{self.event_year}",
            'description': self.description,
            'next_reminder': f"{self.next_reminder.day}/{self.next_reminder.month}/{self.next_reminder.year}",
        }

    def __repr__(self):
        return f"<Reminder(id={self.id}, userId={self.user_id}, description='{self.description}', \
                eventDay={self.event_day}, eventMonth={self.event_month}, eventYear={self.event_year}, \
                reminderDays={self.reminder_days}, nextReminder='{self.next_reminder}')>"


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
        return session.query(Reminder).filter_by(user_id=userId).all()

    def find_by_date(self, date) -> List[Reminder]:
        session = self.Session()
        return session.query(Reminder).filter_by(next_reminder=date).all()

    def delete_by_userid_description(self, user_id, description) -> int:
        session = self.Session()
        try:
            reminders = session.query(Reminder) \
                .filter(Reminder.user_id == user_id, Reminder.description == description) \
                .all()
            for reminder in reminders:
                session.delete(reminder)
            session.commit()
            return len(reminders)
        except NoResultFound:
            return 0

    def get_events(self, user_id):
        query = f"""
            SELECT description, event_day, event_month , event_year, 
            STRING_AGG(reminder_days::text, ',') AS reminder_days_list
            FROM reminder
            WHERE user_id={user_id}
            GROUP BY 1,2,3,4;
        """
        return self.custom_query(query)

    def custom_query(self, sql_query):
        session = self.Session()
        try:
            result = session.execute(text(sql_query))
            return result.fetchall()
        except Exception as e:
            # Handle any exceptions that may occur during the query
            raise Exception(f"Error executing custom query {sql_query}") from e
