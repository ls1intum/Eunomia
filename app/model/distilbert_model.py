import logging

from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
import torch
from typing import List, Tuple
import os

from app.model.model import Model
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


token = os.environ['LLAMA_TOKEN']

class DistilBertModel(Model):
    def __init__(self, model_name="distilbert-base-multilingual-cased", load_directory: str = None, retrain: bool = False):
    # def __init__(self, model_name="distilbert-base-uncased", load_directory: str = None, retrain: bool = False):
        super().__init__()
        if load_directory and not retrain:
            self.load_model(load_directory)
        else:
            logger.info(f"token:{token}")
            self.tokenizer = DistilBertTokenizer.from_pretrained(model_name, token=token)
            logger.info("classifier:")
            self.model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=2, token=token)
            self.device = torch.device("cpu")
            logger.info(f"running on:{self.device} ")
            self.model.to(self.device)
            logger.info("done")

    def train(self, train_data: List[Tuple[str, int]], val_data: List[Tuple[str, int]] = None) -> None:
        train_texts, train_labels = zip(*train_data)
        val_texts, val_labels = zip(*val_data)

        train_encodings = self.tokenizer(list(train_texts), truncation=True, padding=True, max_length=512)
        val_encodings = self.tokenizer(list(val_texts), truncation=True, padding=True, max_length=512)

        class DistilBertDataset(torch.utils.data.Dataset):
            def __init__(self, encodings, labels):
                self.encodings = encodings
                self.labels = labels

            def __getitem__(self, idx):
                item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
                item['labels'] = torch.tensor(self.labels[idx])
                return item

            def __len__(self):
                return len(self.labels)

        train_dataset = DistilBertDataset(train_encodings, list(train_labels))
        val_dataset = DistilBertDataset(val_encodings, list(val_labels))

        training_args = TrainingArguments(
            output_dir='./results',
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=10,
            eval_strategy="epoch",
            save_strategy="epoch",
            use_cpu=True
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
        )

        trainer.train()
        self.is_trained = True

    def predict(self, text: str) -> Tuple[str, float]:
        if not self.is_trained:
            raise ValueError("Model is not trained yet.")

        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512, device=self.device)
        outputs = self.model(**inputs)
        logits = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=-1)
        predicted_class = torch.argmax(probabilities).item()
        confidence = torch.max(probabilities).item()

        return ("sensitive" if predicted_class == 1 else "non-sensitive", confidence)

    def save_model(self, save_directory: str) -> None:
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        self.model.save_pretrained(save_directory)
        self.tokenizer.save_pretrained(save_directory)

    def load_model(self, load_directory: str) -> None:
        self.tokenizer = DistilBertTokenizer.from_pretrained(load_directory)
        self.model = DistilBertForSequenceClassification.from_pretrained(load_directory)
        self.device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
        self.model.to(self.device)
        self.is_trained = True
