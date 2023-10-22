import unittest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.reminder import Reminder, ReminderDAO, Base


class TestReminderDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the database
        cls.engine = create_engine('sqlite:///:memory:')
        cls.Session = sessionmaker(bind=cls.engine)
        Base.metadata.create_all(cls.engine)

    def setUp(self):
        self.dao = ReminderDAO(self.engine)

    def test_create(self):
        # Create a new Reminder object and add it to the database
        reminder = Reminder(user_id=1, description='Pay rent', event_day=1, event_month=6, event_year=2023,
                            reminder_days=7,
                            next_reminder=date(2023, 5, 25))
        # Check that the Reminder was added to the database and has an ID
        self.dao.create(reminder)

    def test_read(self):
        # Add a Reminder to the database
        reminder = Reminder(user_id=1, description='Pay rent', event_day=1, event_month=6, event_year=2023,
                            reminder_days=7,
                            next_reminder=date(2023, 5, 25))
        reminder = self.dao.create(reminder)

        # Read the Reminder back from the database and check its attributes
        db_reminder = self.dao.read(reminder.id)
        self.assertIsNotNone(db_reminder)
        self.assertEqual(db_reminder.user_id, 1)
        self.assertEqual(db_reminder.description, 'Pay rent')
        self.assertEqual(db_reminder.event_day, 1)
        self.assertEqual(db_reminder.event_month, 6)
        self.assertEqual(db_reminder.event_year, 2023)
        self.assertEqual(db_reminder.reminder_days, 7)
        self.assertEqual(db_reminder.next_reminder, date(2023, 5, 25))

    def test_update(self):
        # Add a Reminder to the database
        reminder = Reminder(user_id=1, description='Pay rent', event_day=1, event_month=6, event_year=2023,
                            reminder_days=7,
                            next_reminder=date(2023, 5, 25))
        self.dao.create(reminder)

        # Update the Reminder's attributes and save it to the database
        reminder.description = 'Pay mortgage'
        reminder.reminder_days = 14
        self.dao.update(reminder)

        # Read the Reminder back from the database and check its updated attributes
        db_reminder = self.dao.read(reminder.id)
        self.assertIsNotNone(db_reminder)
        self.assertEqual(db_reminder.description, 'Pay mortgage')
