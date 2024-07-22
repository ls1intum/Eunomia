import logging
import os
from typing import List, Tuple, Optional
from dotenv import load_dotenv
from pymongo import MongoClient, errors
from app.domain.data.email_dto import EmailDTO

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
dotenv_path = os.path.join(os.path.dirname(__file__), '../../development.env')
load_dotenv(dotenv_path)

class EmailDatabase:
    """
    Class to interact with MongoDB to store and retrieve email data.
    """

    def __init__(self):
        """
        Initialize EmailDatabase with MongoDB connection details.
        """
        directory_path = os.getenv('EMAIL_DIRECTORY')
        mongo_uri = os.getenv('MONGO_URI')
        db_name = os.getenv('DB_NAME')
        collection_name = os.getenv('COLLECTION_NAME')
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def store_emails(self, email_data: List[EmailDTO]):
        """
        Store a list of EmailDTO objects in the MongoDB collection.

        :param email_data: List of EmailDTO objects to be stored.
        """
        if not email_data:
            logger.error("No email data to insert.")
            return

        try:
            email_dicts = [email.__dict__ for email in email_data]
            self.collection.insert_many(email_dicts)
            logger.info(
                f"Inserted {len(email_data)} emails into MongoDB collection '{self.collection.name}' in database '{self.db.name}'.")
        except errors.PyMongoError as e:
            logger.error(f"Failed to insert emails: {e}")

    def get_all_email_content(self) -> List[str]:
        """
        Retrieve the plain text body of all emails in the collection.

        :return: List of plain text email bodies.
        """
        try:
            emails = [doc['body_plain'] for doc in self.collection.find()]
            return emails
        except errors.PyMongoError as e:
            logger.error(f"Failed to retrieve email content: {e}")
            return []

    def get_labeled_data(self) -> List[Tuple[str, int]]:
        """
        Retrieve labeled email data for training models.

        :return: List of tuples containing plain text email bodies and their labels.
        """
        try:
            data = [(doc['body_plain'], 1 if doc.get('sensitive') else 0) for doc in self.collection.find()]
            return data
        except errors.PyMongoError as e:
            logger.error(f"Failed to retrieve labeled data: {e}")
            return []
