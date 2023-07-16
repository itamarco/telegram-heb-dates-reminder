import unittest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.reminder import Reminder, ReminderDAO, Base


class TestReminderDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the database
        cls.engine = create_engine('sqlite:///:memory:')
        cls.Session = sessionmaker(bind=cls.engine)
        Base.metadata.create_all(cls.engine)

    def setUp(self):
        # Start a new database session and create a DAO object
        self.session = self.Session()
        self.dao = ReminderDAO(session=self.session)

    def tearDown(self):
        # Roll back any changes made during the test and close the session
        self.session.rollback()
        self.session.close()

    def test_create(self):
        # Create a new Reminder object and add it to the database
        reminder = Reminder(userId=1, description='Pay rent', eventDay=1, eventMonth=6, eventYear=2023, reminderDays=7,
                            nextReminder=date(2023, 5, 25))
        # Check that the Reminder was added to the database and has an ID
        self.dao.create(reminder)

    def test_read(self):
        # Add a Reminder to the database
        reminder = Reminder(userId=1, description='Pay rent', eventDay=1, eventMonth=6, eventYear=2023, reminderDays=7,
                            nextReminder=date(2023, 5, 25))
        self.dao.create(reminder)

        # Read the Reminder back from the database and check its attributes
        db_reminder = self.dao.read(reminder.id)
        self.assertIsNotNone(db_reminder)
        self.assertEqual(db_reminder.userId, 1)
        self.assertEqual(db_reminder.description, 'Pay rent')
        self.assertEqual(db_reminder.eventDay, 1)
        self.assertEqual(db_reminder.eventMonth, 6)
        self.assertEqual(db_reminder.eventYear, 2023)
        self.assertEqual(db_reminder.reminderDays, 7)
        self.assertEqual(db_reminder.nextReminder, date(2023, 5, 25))

    def test_update(self):
        # Add a Reminder to the database
        reminder = Reminder(userId=1, description='Pay rent', eventDay=1, eventMonth=6, eventYear=2023, reminderDays=7,
                            nextReminder=date(2023, 5, 25))
        self.dao.create(reminder)

        # Update the Reminder's attributes and save it to the database
        reminder.description = 'Pay mortgage'
        reminder.reminderDays = 14
        self.dao.update(reminder)

        # Read the Reminder back from the database and check its updated attributes
        db_reminder = self.dao.read(reminder.id)
        self.assertIsNotNone(db_reminder)
        self.assertEqual(db_reminder.description, 'Pay mortgage')
