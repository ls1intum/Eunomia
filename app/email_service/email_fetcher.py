import logging

from app.email_service.email_client import EmailClient
from app.email_service.email_dto import InboxType


class EmailFetcher:
    def __init__(self, email_client: EmailClient):
        self.email_client = email_client
        logging.info("EmailFetcher initialized")

    def fetch_raw_emails(self, folder="inbox"):
        logging.info("EmailFetcher fetching raw emails from folder: %s", folder)
        connection = self.email_client.get_imap_connection()

        connection.select(folder)
        status, messages = connection.search(None, InboxType.Unseen.value)
        email_ids = messages[0].split()

        raw_emails = []
        for email_id in email_ids:
            res, msg = connection.fetch(email_id, "(RFC822)")
            for response_part in msg:
                if isinstance(response_part, tuple):
                    raw_emails.append(response_part[1])
        logging.info("EmailFetcher fetched %d raw emails", len(raw_emails))
        return raw_emails
