from sqlalchemy import create_engine, Column, Integer, String, Date
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

    def delete(self, reminder):
        self.session.delete(reminder)
        self.session.commit()

    def find_by_user(self, userId):
        return self.session.query(Reminder).filter_by(userId=userId).all()
