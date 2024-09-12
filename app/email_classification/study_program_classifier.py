import logging
import os

from app.common.text_cleaner import TextCleaner
from app.email_classification.classifier import Classifier
from app.models.ollama_model import BaseModelClient
from app.prompts.classification_prompts import generate_study_program_classification_prompt


class StudyProgramClassifier(Classifier):
    def __init__(self, model: BaseModelClient):
        super().__init__(model)

    def classify(self, email):
        logging.info("Classifying email...")
        cleansed_text = TextCleaner.cleanse_text(email.body)
        study_programs = self.get_study_programs()
        prompt = generate_study_program_classification_prompt(cleansed_text, study_programs)
        response = self.request_llm(prompt)
        logging.info(f"study program: {response}")
        # return self.parse_classification_result(result)
        return response

    @staticmethod
    def get_study_programs():
        base_folder = os.getenv("STUDY_PROGRAMS_FOLDER")
        study_programs_file = os.path.join(base_folder, "study_programs.txt")
        study_programs = StudyProgramClassifier.load_study_programs(study_programs_file)
        study_programs_str = ", ".join(study_programs)
        return study_programs_str

    @staticmethod
    def parse_classification_result(result):
        classification = result.get("classification", "").lower()
        confidence = int(result.get("confidence", "0%").strip("%"))
        logging.info(f"classification: {classification}, confidence: {confidence}")
        return classification, confidence

    @staticmethod
    def load_study_programs(file_path):
        """
        Load the study programs from study_programs.txt.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Study programs file not found at {file_path}")
        with open(file_path, 'r') as f:
            study_programs = [line.strip() for line in f.readlines() if line.strip()]
        return study_programs

