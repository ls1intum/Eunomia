import logging
import os
import requests
from dotenv import load_dotenv

from app.common.text_cleaner import TextCleaner
from app.email_classification.classifier import Classifier
from app.email_service.email_dto import EmailDTO
from app.models.ollama_model import BaseModelClient
from app.prompts.classification_prompts import generate_classification_prompt


class EmailClassifier(Classifier):
    def __init__(self, model: BaseModelClient):
        super().__init__(model)

    def classify(self, email: EmailDTO):
        logging.info("Classifying email...")
        cleansed_text = TextCleaner.cleanse_text(email.body)
        prompt = generate_classification_prompt(body=cleansed_text, subject=email.subject)
        result = self.request_llm(prompt)
        # return self.parse_classification_result(result)
        return result

    @staticmethod
    def parse_classification_result(result):
        classification = result.get("classification", "").lower()
        confidence = int(result.get("confidence", "0%").strip("%"))
        logging.info(f"classification: {classification}, confidence: {confidence}")
        return classification, confidence
