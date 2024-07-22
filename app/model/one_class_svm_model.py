import logging
import os

import joblib
from typing import List, Tuple

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from app.model.model import Model

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class OneClassSVMModel(Model):
    def __init__(self, load_directory: str = None, retrain: bool = False):
        super().__init__()
        if load_directory and not retrain:
            self.load_model(load_directory)
        else:
            logger.info("retraining:")
            self.model = make_pipeline(TfidfVectorizer(), StandardScaler(with_mean=False),
                                       OneClassSVM(gamma='scale', nu=0.1))

    def train(self, data: List[Tuple[str, int]], val_data: List[Tuple[str, int]] = None) -> None:
        texts, labels = zip(*data)
        non_sensitive_texts = [text for text, label in zip(texts, labels) if label == 0]
        self.model.fit(non_sensitive_texts)
        self.is_trained = True

    def predict(self, text: str) -> Tuple[str, float]:
        if not self.is_trained:
            raise ValueError("Model is not trained yet.")
        prediction = self.model.predict([text])[0]
        decision_function = self.model.decision_function([text])[0]
        if prediction == -1:
            classification = "sensitive"
            certainty = 1 - np.abs(decision_function)
        else:
            classification = "non-sensitive"
            certainty = 1 - np.abs(decision_function)

        return classification, abs(decision_function)

    def save_model(self, save_directory: str) -> None:
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        joblib.dump(self.model, f"{save_directory}/one_class_svm_model.joblib")

    def load_model(self, load_directory: str) -> None:
        self.model = joblib.load(f"{load_directory}/one_class_svm_model.joblib")
        self.is_trained = True
