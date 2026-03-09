from abc import ABC, abstractmethod
from memory.session_memory import SessionMemory


class BasePipeline(ABC):

    def __init__(self):
        self.memory = SessionMemory()

    @abstractmethod
    def run(self, plan):
        pass