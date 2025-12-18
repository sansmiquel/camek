from abc import ABC, abstractmethod
import camek.utils as utils
import pathlib

class Module(ABC):
    def __init__(self,conf_relpath=pathlib.Path):
        self.conf = utils.read_conf(conf_relpath.resolve())
    
    @abstractmethod
    def cycle(self) -> None:
        pass