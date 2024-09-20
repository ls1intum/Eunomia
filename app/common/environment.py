import os

from dotenv import load_dotenv

load_dotenv("./../development.env")


class Config:
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    IMAP_SERVER = os.getenv("IMAP_SERVER")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    IMAP_PORT = os.getenv("IMAP_PORT")
    SMTP_PORT = os.getenv("SMTP_PORT")
    USE_OPENAI = os.getenv("USE_OPENAI", "false")
    USE_AZURE = os.getenv("USE_AZURE", "false")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")
    EMBED_MODEL = os.getenv("EMBED_MODEL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GPU_USER = os.getenv("GPU_USER")
    GPU_PASSWORD = os.getenv("GPU_PASSWORD")
    GPU_HOST = os.getenv("GPU_HOST")
    TEST_EML_PATH = os.getenv("TEST_EML_PATH")
    ANGELOS_URI = os.getenv("ANGELOS_URI")
    ANGELOS_PORT = os.getenv("ANGELOS_PORT")
    ANGELOS_API_KEY = os.getenv("ANGELOS_API_KEY")
    STUDY_PROGRAMS_FOLDER = os.getenv("STUDY_PROGRAMS_FOLDER")
    AZURE_DEPLOYMENT = os.getenv("OPENAI_MODEL_DEPLOYMENT")


config = Config()
