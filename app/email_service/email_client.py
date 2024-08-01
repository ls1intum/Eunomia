import imaplib
import logging
import os
from dotenv import load_dotenv

load_dotenv("./../development.env")


class EmailClient():
    def __init__(self):
        self.username = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.imap_server = os.getenv("IMAP_SERVER")
        self.port = int(os.getenv("EMAIL_PORT"))
        self.connection = None
        logging.info("EmailClient initialized with server: %s", self.imap_server)

    def connect(self):
        try:
            logging.info("Connecting to the email server...")
            self.connection = imaplib.IMAP4_SSL(self.imap_server, self.port)
            self.connection.login(self.username, self.password)
            logging.info("Connected to the email server")
        except imaplib.IMAP4.error as e:
            logging.error("Failed to connect to the server: %s", e)
            raise

    def get_connection(self):
        if not self.connection:
            self.connect()
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.logout()
            logging.info("Connection to the email server closed")