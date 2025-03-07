from abc import ABC, abstractmethod


class Provider(ABC):
    def __init__(self, model_name: str, max_tokens: int = 1024):
        self.model_name = model_name
        self.max_tokens = max_tokens

    @abstractmethod
    def completion(self, prompt: str) -> str:
        raise NotImplementedError
