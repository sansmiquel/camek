from abc import abstractmethod
import math
import numpy as np
import soundfile as sf

from camek.exceptions import CamekFileIOError as CamekFileIOError
from camek.appengine.io.io import AppEngineIO as AppEngineIO


class AppEngineInputFile(AppEngineIO):
    def __init__(self,conf=dict):
        super().__init__(conf=conf)  

    @abstractmethod
    def data_transfer(self):
        pass

class AppEngineInputEntireFile(AppEngineInputFile):
    def __init__(self,conf=dict):
        super().__init__(conf=conf)
        pass

    def data_transfer(self):
        pass

class AppEngineInputChunkedFile(AppEngineInputFile):
    def __init__(self,conf=dict):
        super().__init__(conf=conf)

    def data_transfer(self):
        pass

        return None

class AppEngineOutputFile(AppEngineIO):
    def __init__(self,conf=dict):
        super().__init__(conf=conf)

    @abstractmethod
    def data_transfer(self):
        pass

class AppEngineOutputEntireFile(AppEngineOutputFile):
    def __init__(self,conf=dict):
        super().__init__(conf=conf)

    def data_transfer(self):
        pass

class AppEngineOutputChunkedFile(AppEngineOutputFile):
    def __init__(self,conf=dict):
        super().__init__(conf=conf)

    def data_transfer(self):
        pass