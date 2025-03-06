from abc import ABC, abstractmethod


class Provider(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def completion(self, prompt: str) -> str:
        raise NotImplementedError
