from abc import ABC, abstractmethod
from typing import List, Tuple


class Preprocessor(ABC):
    @abstractmethod
    def preprocess(self, text: str) -> str:
        """
        Preprocess the input text.

        :param text: The text to preprocess.
        :return: A list of processed tokens or terms.
        """
        pass