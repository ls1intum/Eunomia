import logging

from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, QuantoConfig
import torch
from typing import List, Tuple
import os

from app.model.model import Model

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
token = os.environ['LLAMA_TOKEN']


class LlamaClassifier(Model):
    # def __init__(self, model_name="meta-llama/LLaMA-3.1-8B", load_directory: str = None, retrain: bool = False):
    def __init__(self, model_name="meta-llama/Meta-Llama-3.1-8B", load_directory: str = None, retrain: bool = False):
        super().__init__()
        if load_directory and not retrain:
            self.load_model(load_directory)
        else:
            logger.info(f"the token retrieval is working: {token}")
            # self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B")
            # self.model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3.1-8B")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)

            try:
                self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2,
                                                                                token=token,
                                                                                device_map="mps",
                                                                                quantization_config=QuantoConfig(
                                                                                    weights="int4"))
            except Exception as e:
                print(f"Attempt failed: {e}")
            self.is_trained = False

    def train(self, data: List[Tuple[str, int]], val_data: List[Tuple[str, int]] = None) -> None:
        texts, labels = zip(*data)
        train_encodings = self.tokenizer(list(texts), truncation=True, padding=True, max_length=512)
        train_labels = list(labels)

        class LlamaDataset(torch.utils.data.Dataset):
            def __init__(self, encodings, labels):
                self.encodings = encodings
                self.labels = labels

            def __getitem__(self, idx):
                item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
                item['labels'] = torch.tensor(self.labels[idx])
                return item

            def __len__(self):
                return len(self.labels)

        train_dataset = LlamaDataset(train_encodings, train_labels)

        training_args = TrainingArguments(
            output_dir='./results',
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=10,
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
        )

        trainer.train()
        self.is_trained = True

    def predict(self, text: str) -> Tuple[str, float]:
        if not self.is_trained:
            raise ValueError("Model is not trained yet.")

        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
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
        self.tokenizer = AutoTokenizer.from_pretrained(load_directory)
        self.model = AutoModelForSequenceClassification.from_pretrained(load_directory)
        self.is_trained = True
