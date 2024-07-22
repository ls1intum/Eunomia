import re

from app.orchestration.preprocessor.preprocessor import Preprocessor


class SimplePreprocessor(Preprocessor):
    def preprocess(self, text: str) -> str:
        text = re.sub(r'\W', ' ', text)
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        return text.strip()