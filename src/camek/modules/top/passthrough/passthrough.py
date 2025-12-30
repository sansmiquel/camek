from abc import abstractmethod
from camek.modules.builtin import TopModule
import pathlib
import math
import numpy as np
import soundfile as sf

class TopLevelProcessingModule(TopModule):
    def __init__(self,conf_relpath: str):
       super().__init__(conf_relpath=conf_relpath)
       self.output = None
    
    def get_status(self) -> bool:
        return True
    def get_output(self) -> np.array:
        return self.output
    def cycle(self, input: np.array) -> None:
        self.output = input