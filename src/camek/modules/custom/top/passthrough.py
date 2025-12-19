from abc import abstractmethod
from camek.modules.module import TopModule
import pathlib
import math
import numpy as np
import soundfile as sf

class TopLevelProcessingModule(TopModule):
    def __init__(self,conf_relpath: pathlib.Path):
       super().__init__(conf_relpath=conf_relpath)
       self.x = None

    def get_status(self) -> None:
        pass
    def get_output(self):
        pass
    #def cycle(self, x: np.array) -> None:
    def cycle(self) -> None:
        self.x = None