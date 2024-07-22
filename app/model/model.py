from abc import ABC, abstractmethod
from typing import List, Tuple


class Model(ABC):
    def __init__(self):
        self.is_trained = False

    @abstractmethod
    def train(self, data: List[Tuple[str, int]], val_data: List[Tuple[str, int]] = None) -> None:
        """
        Train the model with labeled data.

        :param val_data: validation data list of tuples containing text data and their corresponding labels
        :param data: List of tuples containing text data and their corresponding labels.
        """
        pass

    @abstractmethod
    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict the label of the given text.

        :param text: The input text to classify.
        :return: A tuple containing the predicted label and the confidence score.
        """
        pass

    @abstractmethod
    def save_model(self, save_directory: str) -> None:
        """
        Save the model to a certain directory

        :param save_directory: The directory where the model should be saved.
        :return:
        """
        pass

    @abstractmethod
    def load_model(self, load_directory: str) -> None:
        """
            load the model from a certain directory

            :param load_directory: The directory where the model should be loaded from .
            :return:
        """
        pass