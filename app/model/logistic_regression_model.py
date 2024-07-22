import logging
from typing import List, Tuple

import joblib

from app.model.model import Model
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class LogisticRegressionModel(Model):
    def __init__(self, load_directory: str = None, retrain: bool = False):
        super().__init__()
        if load_directory and not retrain:
            self.load_model(load_directory)
        else:
            logger.info("retraining:")
            self.model = make_pipeline(TfidfVectorizer(), LogisticRegression())

    def train(self, data: List[Tuple[str, int]], val_data: List[Tuple[str, int]] = None) -> None:
        texts, labels = zip(*data)
        self.model.fit(texts, labels)
        self.is_trained = True

    def predict(self, text: str) -> Tuple[str, float]:
        if not self.is_trained:
            raise ValueError("Model is not trained yet.")
        pred = self.model.predict([text])[0]
        prob = max(self.model.predict_proba([text])[0])
        return "sensitive" if pred else "non-sensitive", prob

    def save_model(self, save_directory: str) -> None:
        joblib.dump(self.model, f"{save_directory}/logistic_regression_model.joblib")

    def load_model(self, load_directory: str) -> None:
        self.model = joblib.load(f"{load_directory}/logistic_regression_model.joblib")
        self.is_trained = True
