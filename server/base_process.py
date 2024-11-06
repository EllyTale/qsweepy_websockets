from abc import ABC, abstractmethod

class BaseProcess(ABC):

    @abstractmethod
    def run(self):
        pass