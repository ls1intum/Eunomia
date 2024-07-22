import logging
import os
from app.database.email_database import EmailDatabase
from app.orchestration.email_archiver.email_parser import EmailParser
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv("../../../development.env")


def main():
    directory_path = os.getenv('EMAIL_DIRECTORY')
    logger.info(f"Lets parse: ")
    logger.info(f"Email directory: {directory_path} ")
    # parser = EmailParser()
    # emails = parser.process_eml_files_in_directory(directory_path, False)
    # logger.info(f"Get an example: ")
    # logger.info(f"Emails: {emails[0]}")
    # storage = EmailDatabase()
    # storage.store_emails(emails)

if __name__ == '__main__':
    main()
