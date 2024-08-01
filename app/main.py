import logging
import os
import time

from dotenv import load_dotenv

from app.email_classification.email_classifier import EmailClassifier
from app.email_service.email_client import EmailClient
from app.email_service.email_fetcher import EmailFetcher
from app.email_service.email_processor import EmailProcessor
from app.common.logging_config import setup_logging
from app.models.ollama_model import OllamaModel

load_dotenv("./../development.env")

def main():
    setup_logging()
    logging.info("Application started")
    email_client = EmailClient()
    email_fetcher = EmailFetcher(email_client)
    email_processor = EmailProcessor()
    api_key = os.getenv("LLAMA_MODEL_TOKEN")
    url = os.getenv("LLAMA_MODEL_URI")
    llama = OllamaModel(model="azureai", api_key=api_key, url=url)
    email_classifier = EmailClassifier(llama)

    try:
        email_client.connect()
        while True:
            logging.info("Fetching new emails...")
            raw_emails = email_fetcher.fetch_raw_emails()
            emails = email_processor.process_raw_emails(raw_emails)
            for email in emails:
                email_classifier.classify_email(email)
            logging.info("Sleeping for 60 seconds before next fetch")
            time.sleep(60)

    except Exception as e:
        logging.error("An error occurred: %s", e)
    finally:
        email_client.close_connection()
        logging.info("Application finished")

if __name__ == "__main__":
    main()
