import logging
import os
from typing import Tuple

from sklearn.model_selection import train_test_split

from app.common.singleton import Singleton
from app.database.email_database import EmailDatabase
from app.model.bert_model import BERTModel
from app.model.distilbert_model import DistilBertModel
from app.model.few_shot_model import FewShotModel
from app.model.llama_model import LlamaClassifier
from app.model.logistic_regression_model import LogisticRegressionModel
from app.model.model import Model
from app.model.one_class_svm_model import OneClassSVMModel
from app.model.zero_shot_model import ZeroShotModel
from app.orchestration.preprocessor.preprocessor import Preprocessor

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ModelManager(metaclass=Singleton):
    def __init__(self, email_db: EmailDatabase, preprocessor: Preprocessor, model_name: str, retrain: bool = False,
                 model_directory: str = "./models"):
        self.email_database = email_db
        self.preprocessor = preprocessor
        self.retrain = retrain
        self.model_name = model_name
        self.model_directory = model_directory
        self.model_path = os.path.join(model_directory, model_name)
        self.model = self.initialize_model()

    def initialize_model(self) -> Model:
        load_directory = self.model_path if os.path.exists(self.model_path) else None
        if self.model_name == "logistic_regression":
            model = LogisticRegressionModel(load_directory=load_directory, retrain=self.retrain)
        elif self.model_name == "bert":
            model = BERTModel(load_directory=load_directory, retrain=self.retrain)
        elif self.model_name == "zero_shot":
            model = ZeroShotModel(load_directory=load_directory, retrain=self.retrain)
        elif self.model_name == "one_class_svm":
            model = OneClassSVMModel(load_directory=load_directory, retrain=self.retrain)
        elif self.model_name == "few_shot":
            model = FewShotModel(load_directory=load_directory, retrain=self.retrain)
        elif self.model_name == "llama":
            model = LlamaClassifier(load_directory=load_directory, retrain=self.retrain)
        elif self.model_name == "distilbert":
            model = DistilBertModel(load_directory=load_directory, retrain=self.retrain)
        else:
            raise ValueError(f"Unsupported model type: {self.model_name}")

        return model

    def save_model(self) -> None:
        if not os.path.exists(self.model_directory):
            logger.info("create new directory")
            os.makedirs(self.model_directory)
        logger.info(f"saving model under {self.model_path}")
        self.model.save_model(self.model_path)

    def get_model(self) -> Model:
        return self.model

    def train_model(self):
        labeled_data = self.email_database.get_labeled_data()
        if isinstance(self.model, ZeroShotModel) or isinstance(self.model, FewShotModel):
            logger.info("Zero or few shot without validation data")
            logger.info(f"Data {labeled_data[0]}")
            self.model.train(labeled_data)
        else:
            train_data, val_data = train_test_split(labeled_data, test_size=0.2, random_state=42)
            self.model.train(train_data, val_data)

        logger.info(f"Got {len(labeled_data)} of labled emails and start trainig")
        self.save_model()

    def classify_email(self, email_text: str) -> Tuple[str, float]:
        logger.info(f"Classify emails")
        processed_text = self.preprocessor.preprocess(email_text)
        return self.model.predict(processed_text)
