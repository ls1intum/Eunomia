import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.email_service.email_dto import EmailDTO, InboxType


class EmailService:
    def __init__(self, email_client):
        self.email_client = email_client

    def fetch_raw_emails(self, folder="inbox"):
        logging.info("EmailFetcher fetching raw emails from folder: %s", folder)
        connection = self.email_client.get_imap_connection()

        connection.select(folder)
        status, messages = connection.search(None, InboxType.Unseen.value, InboxType.Unflagged.value)

        email_ids = messages[0].split()

        raw_emails = []
        for email_id in email_ids:
            res, msg = connection.fetch(email_id, "(RFC822)")
            for response_part in msg:
                if isinstance(response_part, tuple):
                    raw_emails.append(response_part[1])
        logging.info("EmailFetcher fetched %d raw emails", len(raw_emails))
        return raw_emails

    def search_by_message_id(self, message_id):
        imap_conn = self.email_client.get_imap_connection()
        imap_conn.select('inbox')
        logging.info(f"Searching for message with ID: {message_id}...")

        result, data = imap_conn.uid('SEARCH', None, f'(HEADER Message-ID "{message_id}")')

        if result == 'OK':
            email_uids = data[0].split()
            if email_uids:
                logging.info(f"Found email with UID: {email_uids[-1]}")
                return email_uids[-1]
            else:
                logging.warning(f"No email found with Message-ID: {message_id}")
                return None
        else:
            logging.error(f"Search failed for Message-ID: {message_id}")
            return None

    def flag_email(self, message_id):
        email_uid = self.search_by_message_id(message_id)
        if email_uid:
            # Set both \Flagged and \Unseen flags
            imap_conn = self.email_client.get_imap_connection()

            result, response = imap_conn.uid('STORE', email_uid, '+FLAGS', r'(\Flagged \Seen)')

            if result == 'OK':
                # Now remove the \Seen flag to keep it unread
                imap_conn.uid('STORE', email_uid, '-FLAGS', r'(\Seen)')
                logging.info(f"Email with UID {email_uid} has been successfully flagged and set to unread.")
            else:
                logging.error(f"Failed to flag the email with UID {email_uid}.")
        else:
            logging.error("Invalid UID. No email to flag.")

    def send_reply_email(self, original_email: EmailDTO, reply_body):
        smtp_conn = self.email_client.get_smtp_connection()

        # Extract headers from the original email
        from_address = original_email.from_address
        to_address = self.email_client.username
        subject = "Re: " + original_email.subject
        message_id = original_email.message_id

        # Create the reply email
        msg = MIMEMultipart()
        msg['From'] = to_address
        msg['To'] = from_address
        msg['Subject'] = subject
        msg['In-Reply-To'] = message_id
        msg['References'] = message_id
        # Attach the reply body
        msg.attach(MIMEText(reply_body, 'plain'))

        try:
            smtp_conn.send_message(msg)
            logging.info("Reply email sent to %s", from_address)
        except (smtplib.SMTPException, ConnectionError) as e:
            logging.error("Failed to send email due to %s. Attempting to reconnect and resend.", e)
