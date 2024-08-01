import logging
import os
import requests
from dotenv import load_dotenv

from app.common.text_cleaner import TextCleaner
from app.email_service.email_dto import EmailDTO
from app.models.ollama_model import OllamaModel


class EmailClassifier:
    def __init__(self, model: OllamaModel):
        self.model = model
    def classify_email(self, email: EmailDTO):
        logging.info("Classifying email...")
        cleansed_text = TextCleaner.cleanse_text(email.body)
        result = self.request_llm(email_body=cleansed_text, email_subject=email.subject)
        return self.parse_classification_result(result)

    def request_llm(self, email_body, email_subject):
        logging.info(f"Requesting LLM")
        return self.model.complete(email_body, email_subject)

    @staticmethod
    def parse_classification_result(result):
        classification = result.get("classification", "").lower()
        confidence = int(result.get("confidence", "0%").strip("%"))
        logging.info(f"classification: {classification}, confidence: {confidence}")
        return classification, confidence
