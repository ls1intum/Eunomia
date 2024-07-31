import logging
import os
from typing import Tuple, List
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch

from app.domain.data.email_dataset import EmailDataset
from app.model.model import Model

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class BERTModel(Model):
    def __init__(self, model_name="bert-base-multilingual-cased", load_directory: str = None, retrain: bool = False):
    # def __init__(self, model_name="bert-base-german-cased", load_directory: str = None, retrain: bool = False):
        super().__init__()
        if load_directory and not retrain:
            self.load_model(load_directory)
        else:
            logger.info("retraining:")
            self.tokenizer = BertTokenizer.from_pretrained(model_name)
            self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)
            self.device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
            logger.info(f"running on:{self.device} ")
            self.model.to(self.device)
            self.is_trained = False

    def train(self, data: List[Tuple[str, int]], val_data: List[Tuple[str, int]] = None) -> None:
        texts, labels = zip(*data)
        val_texts, val_labels = zip(*val_data)

        train_dataset = EmailDataset(
            texts=texts,
            labels=labels,
            tokenizer=self.tokenizer,
            max_len=128
        )

        eval_dataset = EmailDataset(
            texts=val_texts,
            labels=val_labels,
            tokenizer=self.tokenizer,
            max_len=128
        )

        training_args = TrainingArguments(
            output_dir='./results',
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=10,
            save_steps=10,
            save_total_limit=2,
            eval_strategy="steps",
            eval_steps=10,
            no_cuda=True
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset
        )

        trainer.train()
        self.is_trained = True

    def predict(self, text: str) -> Tuple[str, float]:
        if not self.is_trained:
            raise ValueError("Model is not trained yet.")

        inputs = self.tokenizer(text, return_tensors='pt', padding='max_length', truncation=True, max_length=128)
        outputs = self.model(**inputs)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(probabilities).item()
        confidence = torch.max(probabilities).item()
        return "sensitive" if predicted_class == 1 else "non-sensitive", confidence

    def save_model(self, save_directory: str) -> None:
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        self.model.save_pretrained(save_directory)
        self.tokenizer.save_pretrained(save_directory)

    def load_model(self, load_directory: str) -> None:
        self.tokenizer = BertTokenizer.from_pretrained(load_directory)
        self.model = BertForSequenceClassification.from_pretrained(load_directory)
        self.device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
        self.model.to(self.device)
        self.is_trained = True
