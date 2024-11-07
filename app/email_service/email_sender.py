import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.email_service.email_dto import EmailDTO


class EmailSender:
    def __init__(self, email_client):
        self.email_client = email_client

    def send_reply_email(self, original_email: EmailDTO, reply_body):
        if not self.email_client.smtp_connection:
            self.email_client.connect_smtp()

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
            self.email_client.smtp_connection.send_message(msg)
            logging.info("Reply email sent to %s", from_address)
        except smtplib.SMTPException as e:
            logging.error("Failed to send reply email: %s", e)
            self.email_client.flag_email(original_email.message_id)
            raise
