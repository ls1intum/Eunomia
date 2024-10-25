import os

from dotenv import load_dotenv

if os.getenv("ENVIRONMENT") == "development":
    load_dotenv("./../development.env")


class Config:
    USE_OPENAI = os.getenv("USE_OPENAI", "false")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")
    API_KEY = os.getenv("LLAMA_MODEL_TOKEN")
    URL = os.getenv("LLAMA_MODEL_URI")

    OLLAMA_MODEL = os.getenv("GPU_MODEL")
    OLLAMA_URL = os.getenv("GPU_URL")
    GPU_USER = os.getenv("GPU_USER")
    GPU_PASSWORD = os.getenv("GPU_PASSWORD")
    GPU_HOST = os.getenv("GPU_HOST")

    TEST_EML_PATH = os.getenv("TEST_EML_PATH")

    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    IMAP_SERVER = os.getenv("IMAP_SERVER")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    IMAP_PORT = os.getenv("IMAP_PORT")
    SMTP_PORT = os.getenv("SMTP_PORT")

    ANGELOS_URI = os.getenv("ANGELOS_URI")
    ANGELOS_PORT = os.getenv("ANGELOS_PORT")
    STUDY_PROGRAMS_FOLDER = os.getenv("STUDY_PROGRAMS_FOLDER")


config = Config()
