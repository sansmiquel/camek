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

    def cycle(self, x: np.array) -> None:
        self.x = x