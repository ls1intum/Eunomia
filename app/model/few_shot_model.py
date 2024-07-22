import logging
from typing import List, Tuple

import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
import os

from app.domain.data.few_shot_dataset import FewShotDataset
from app.model.model import Model

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class FewShotModel(Model):
    def __init__(self, model_name="t5-small", load_directory: str = None, retrain: bool = False):
        super().__init__()
        if load_directory and os.path.exists(load_directory) and not retrain:
            self.load_model(load_directory)
        else:
            logger.info("retraining:")
            self.tokenizer = T5Tokenizer.from_pretrained(model_name)
            self.model = T5ForConditionalGeneration.from_pretrained(model_name)

    def train(self, data: List[Tuple[str, int]], val_data: List[Tuple[str, int]] = None) -> None:
        texts, labels = zip(*data)
        formatted_texts = [f"classify: {text}" for text in texts]
        formatted_labels = [f"sensitive" if label == 1 else "non-sensitive" for label in labels]
        logger.info(formatted_labels)
        logger.info(formatted_texts)
        train_encodings = self.tokenizer(list(formatted_texts), truncation=True, padding=True, max_length=512)
        train_labels = self.tokenizer(list(formatted_labels), truncation=True, padding=True, max_length=10)

        train_dataset = FewShotDataset(train_encodings, train_labels)

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

        input_text = f"classify: {text}"
        inputs = self.tokenizer(input_text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.model.generate(inputs['input_ids'], return_dict_in_generate=True, output_scores=True,
                                          max_length=10)
            prediction = self.tokenizer.decode(outputs.sequences[0], skip_special_tokens=True).strip()

            # Calculate the certainty score using the logits
            scores = outputs.scores[0][0]
            probabilities = torch.nn.functional.softmax(scores, dim=-1)
            certainty = torch.max(probabilities).item()

        # Ensure the prediction is either "sensitive" or "non-sensitive"
        if "sensitive" in prediction.lower():
            classification = "sensitive"
        elif "non-sensitive" in prediction.lower():
            classification = "non-sensitive"
        else:
            classification = "unknown"

        return classification, certainty

    def save_model(self, save_directory: str) -> None:
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        self.model.save_pretrained(save_directory)
        self.tokenizer.save_pretrained(save_directory)

    def load_model(self, load_directory: str) -> None:
        self.tokenizer = T5Tokenizer.from_pretrained(load_directory)
        self.model = T5ForConditionalGeneration.from_pretrained(load_directory)
        self.is_trained = True