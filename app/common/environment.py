import os

from dotenv import load_dotenv

if os.getenv("ENVIRONMENT") == "development":
    load_dotenv("./../development.env")


class Config:
    # email
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    IMAP_SERVER = os.getenv("IMAP_SERVER")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    IMAP_PORT = os.getenv("IMAP_PORT")
    SMTP_PORT = os.getenv("SMTP_PORT")

    # appliocation flow
    USE_OPENAI = os.getenv("USE_OPENAI", "false")
    USE_AZURE = os.getenv("USE_AZURE", "false")

    # gpu
    GPU_USER = os.getenv("GPU_USER")
    GPU_PASSWORD = os.getenv("GPU_PASSWORD")
    GPU_HOST = os.getenv("GPU_HOST")
    GPU_MODEL = os.getenv("GPU_MODEL")
    GPU_URL = os.getenv("GPU_URL")

    # test
    TEST_EML_PATH = os.getenv("TEST_EML_PATH")

    # angelos
    ANGELOS_URI = os.getenv("ANGELOS_URI")
    ANGELOS_PORT = os.getenv("ANGELOS_PORT")

    # openai
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")
    AZURE_DEPLOYMENT = os.getenv("OPENAI_MODEL_DEPLOYMENT")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    STUDY_PROGRAMS_FOLDER = os.getenv("STUDY_PROGRAMS_FOLDER")


config = Config()
