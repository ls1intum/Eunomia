import logging
import os
import time
import traceback

from dotenv import load_dotenv

from app.common.logging_config import setup_logging
from app.email_responder.email_responder import EmailResponder

if os.getenv("ENVIRONMENT") == "development":
    load_dotenv("./../development.env")


def main():
    setup_logging()
    logging.info("Application started")
    try:
        email_responder = EmailResponder()
        email_responder.start()
    except Exception as e:
        tb = traceback.format_exc()
        logging.error("An error occurred: %s", e)
        logging.error("Traceback:\n%s", tb)
        raise
    finally:
        logging.info("Application finished")


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception:
            logging.info("Restarting application after an exception...")
            time.sleep(5)
