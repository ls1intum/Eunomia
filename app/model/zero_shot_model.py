import logging
from typing import Tuple, List

from transformers import pipeline
import os

from app.model.model import Model

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
class ZeroShotModel(Model):
    def __init__(self, model_name="facebook/bart-large-mnli", load_directory: str = None, retrain: bool = False):
        super().__init__()
        if load_directory and os.path.exists(load_directory) and not retrain:
            self.load_model(load_directory)
        else:
            logger.info("retraining:")
            self.classifier = pipeline("zero-shot-classification", model=model_name)
            self.model_path = load_directory

    def train(self, data: List[Tuple[str, int]], val_data: List[Tuple[str, int]] = None) -> None:
        pass

    def predict(self, text):
        if not hasattr(self, 'classifier'):
            raise ValueError("Model is not loaded yet.")
        candidate_labels = ["sensitive", "non-sensitive"]
        result = self.classifier(text, candidate_labels)
        label = result['labels'][0]
        score = result['scores'][0]
        return label, score

    def save_model(self, save_directory: str) -> None:
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        self.classifier.model.save_pretrained(save_directory)
        self.classifier.tokenizer.save_pretrained(save_directory)

    def load_model(self, load_directory: str) -> None:
        self.classifier = pipeline("zero-shot-classification", model=load_directory)
        self.is_trained = True
