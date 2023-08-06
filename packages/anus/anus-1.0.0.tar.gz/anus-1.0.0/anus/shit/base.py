from abc import ABC, abstractmethod


class ShitBase(ABC):
    @abstractmethod
    def stink(self):
        pass
