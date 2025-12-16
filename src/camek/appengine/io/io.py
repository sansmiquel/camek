from abc import ABC, abstractmethod

class AppEngineIO(ABC):
    def __init__(self,conf=dict):
        self.conf = conf
    
    @abstractmethod
    def data_transfer(self) -> None:
        pass
