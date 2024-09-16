import os

from dotenv import load_dotenv

load_dotenv("./../development.env")


class Config:
    WEAVIATE_URL = os.getenv("WEAVIATE_URL", "localhost")
    WEAVIATE_PORT = os.getenv("WEAVIATE_PORT", "8001")
    USE_OPENAI = os.getenv("USE_OPENAI", "false")
    OLLAMA_URL = os.getenv("GPU_URL")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")
    EMBED_MODEL = os.getenv("EMBED_MODEL")
    API_KEY = os.getenv("LLAMA_MODEL_TOKEN")
    URL = os.getenv("LLAMA_MODEL_URI")
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
    ANGELOS_API_KEY = os.getenv("ANGELOS_API_KEY")
    STUDY_PROGRAMS_FOLDER = os.getenv("STUDY_PROGRAMS_FOLDER")


config = Config()
