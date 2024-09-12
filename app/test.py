import logging
import os
from email import policy
from email.parser import BytesParser

from dotenv import load_dotenv

from app.common.logging_config import setup_logging
from app.email_responder.email_responder import EmailResponder

# Configuration
load_dotenv("./../development.env")
eml_folder_path = os.getenv("TEST_EML_PATH")


def process_eml_files():
    email_responder = EmailResponder()
    for i, filename in enumerate(os.listdir(eml_folder_path), start=1):
        if filename.endswith('.eml'):
            eml_file_path = os.path.join(eml_folder_path, filename)
            with open(eml_file_path, 'rb') as f:
                eml_data = f.read()

            # Parse the .eml file
            email_message = BytesParser(policy=policy.default).parsebytes(eml_data)
            raw_emails = [email_message.as_bytes()]
            emails = email_responder.email_processor.process_raw_emails(raw_emails)
            for email in emails:
                classification, confidence = email_responder.email_classifier.classify(email)
                classification1, confidence1 = email_responder.study_program_classifier.classify(email)
                logging.info(f"email {i}: {email.subject} with classification: {classification.strip()}")
                logging.info(f"email {i}: {email.subject} with classification: {classification1.strip()}")


if __name__ == "__main__":
    setup_logging()
    logging.info("Application started")
    process_eml_files()
