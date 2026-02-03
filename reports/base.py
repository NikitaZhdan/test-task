from abc import ABC, abstractmethod


class BaseReport(ABC):
    @abstractmethod
    def generate(self, data):
        pass

    @abstractmethod
    def get_headers(self):
        pass
