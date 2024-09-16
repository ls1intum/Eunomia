

class BaseModelClient:
    def __init__(self, model: str):
        self.model = model

    def complete(self, prompt: []) -> (str, float):
        raise NotImplementedError("This method should be implemented by subclasses.")
