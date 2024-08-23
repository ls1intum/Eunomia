import imaplib
import logging
import os
import smtplib

from dotenv import load_dotenv

load_dotenv("./../development.env")


class EmailClient:
    def __init__(self):
        self.username = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.imap_server = os.getenv("IMAP_SERVER")
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.imap_port = int(os.getenv("IMAP_PORT"))
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.imap_connection = None
        self.smtp_connection = None
        logging.info("EmailClient initialized")

    def get_imap_connection(self):
        if not self.imap_connection:
            self.connect_imap()
        return self.imap_connection

    def get_smtp_connection(self):
        if not self.smtp_connection:
            self.connect_smtp()
        return self.smtp_connection

    def connect_imap(self):
        try:
            logging.info("Connecting to the IMAP server...")
            self.imap_connection = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            self.imap_connection.login(self.username, self.password)
            logging.info("Connected to the IMAP server")
        except imaplib.IMAP4.error as e:
            logging.error("Failed to connect to the IMAP server: %s", e)
            raise

    def connect_smtp(self):
        try:
            logging.info(f"Connecting to the SMTP server...")
            self.smtp_connection = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            self.smtp_connection.login(self.username, self.password)
            logging.info("Connected to the SMTP server")
        except smtplib.SMTPException as e:
            logging.error("Failed to connect to the SMTP server: %s", e)
            raise

    def close_connections(self):
        if self.imap_connection:
            self.imap_connection.logout()
            logging.info("IMAP connection closed")
        if self.smtp_connection:
            self.smtp_connection.quit()
            logging.info("SMTP connection closed")

    def connect(self):
        self.connect_imap()
        self.connect_smtp()
