import logging
import time
import traceback

from app.email_classification.email_classifier import EmailClassifier
from app.email_classification.response_service import ResponseService
from app.email_service.email_client import EmailClient
from app.email_service.email_fetcher import EmailFetcher
from app.email_service.email_processor import EmailProcessor
from app.email_service.email_sender import EmailSender
from app.models.model_loader import get_model_client


class EmailResponder:
    def __init__(self):
        self.email_client = EmailClient()
        self.email_fetcher = EmailFetcher(self.email_client)
        self.email_processor = EmailProcessor()
        self.email_sender = EmailSender(self.email_client)
        # self.model_api_key = os.getenv("LLAMA_MODEL_TOKEN")
        # self.model_url = os.getenv("LLAMA_MODEL_URI")
        self.llama = get_model_client()
        self.email_classifier = EmailClassifier(self.llama)
        self.response_service = ResponseService()
        self.MAX_RETRIES = 3
        self.RETRY_DELAY = 2
        logging.info("EmailResponder initialized")

    def start(self):
        try:
            self.email_client.connect()
            while True:
                logging.info("Fetching new emails...")
                raw_emails = self.email_fetcher.fetch_raw_emails()
                if not raw_emails:
                    logging.info("No new emails. Sleeping briefly before next check.")
                    time.sleep(30)
                    continue
                emails = self.email_processor.process_raw_emails(raw_emails)
                for email in emails:
                    if email.in_reply_to is None and len(email.references) == 0 and (
                            email.spam == "NO" or email.spam is None):
                        classification, language, study_program = self.classify_with_retries(email)
                        self.handle_classification(email, classification, study_program, language)
                    else:
                        self.email_client.flag_email(email.message_id)
                logging.info("Sleeping for 60 seconds before next fetch")
                time.sleep(60)
        except Exception as e:
            tb = traceback.format_exc()
            logging.error("An error occurred: %s", e)
            logging.error("Traceback:\n%s", tb)
        finally:
            self.email_client.close_connections()

    def handle_classification(self, email, classification, study_program, language):
        # response_content = self.generate_email_response(email, classification)
        response_content = None
        if classification.strip().lower() == "non-sensitive":
            logging.info("should get a response now ")
            payload = {
                "message": email.body,
                "study_program": study_program,
                "language": language,
            }
            response_content = self.response_service.get_response(payload)
            # logging.info("api call to angelos was made")
            # response_content = {'answer': "Hallo kollege, hier haste deine antwort"}
        if response_content:
            self.email_sender.send_reply_email(original_email=email, reply_body=response_content['answer'])
        else:
            logging.info("No proper answer can be found or it is classified as sensitive")
            self.email_client.flag_email(email.message_id)

    def classify_with_retries(self, email):
        """Attempts to classify an email with retries."""
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                return self.email_classifier.classify(email)
            except Exception as e:
                tb = traceback.format_exc()
                logging.error("Error on attempt %d for email: %s", attempt, email)
                logging.error("An error occurred: %s", e)
                logging.error("Traceback:\n%s", tb)

                # If max retries reached, raise the exception
                if attempt == self.MAX_RETRIES:
                    logging.error("Max retries reached for email: %s. Skipping this email.", email)
                    raise
                else:
                    # Optionally add a delay between retries
                    logging.info("Retrying... (attempt %d of %d)", attempt, self.MAX_RETRIES)
                    time.sleep(self.RETRY_DELAY)

    def generate_email_response(self, email, classification):
        # This method generates a response based on the classification
        response = f"Generated response for {email.subject} with classification: {classification}"
        return response


if __name__ == "__main__":
    email_responder = EmailResponder()
    email_responder.start()
