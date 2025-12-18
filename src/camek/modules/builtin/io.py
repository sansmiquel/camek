
from abc import abstractmethod
from camek.modules.module import Module
import pathlib
import math
import numpy as np
import soundfile as sf

class AudioIO(Module):
    def __init__(self,conf_relpath=pathlib.Path):
       super().__init__(conf_relpath=conf_relpath)

    @abstractmethod
    def get_status(self):
        pass

class AudioInput(AudioIO):
    def __init__(self,conf_relpath=pathlib.Path):
        super().__init__(conf_relpath=conf_relpath)  

    def get_status(self):
        pass
    def cycle(self):
        pass

class AudioOutput(AudioIO):
    def __init__(self,conf_relpath=pathlib.Path):
        super().__init__(conf_relpath=conf_relpath)

    def get_status(self):
        pass
    def cycle(self):
        pass

# class AudioInputFile(AudioIO):
#     def __init__(self,conf_relpath=pathlib.Path):
#         super().__init__(conf_relpath=conf_relpath)  

#     def cycle(self):
#         pass

# class AppEngineInputEntireFile(AppEngineInputFile):
#     def __init__(self,conf_relpath=pathlib.Path):
#         super().__init__(conf_relpath=conf_relpath)
#         pass

#     def cycle(self):
#         pass

# class AppEngineInputChunkedFile(AppEngineInputFile):
#     def __init__(self,conf_relpath=pathlib.Path):
#         super().__init__(conf_relpath=conf_relpath)

#     def cycle(self):
#         pass

#         return None



# class AudioOutputFile(AudioIO):
#     def __init__(self,conf_relpath=pathlib.Path):
#         super().__init__(conf_relpath=conf_relpath)

#     def cycle(self):
#         pass

# class AppEngineOutputEntireFile(AppEngineOutputFile):
#     def __init__(self,conf_relpath=pathlib.Path):
#         super().__init__(conf_relpath=conf_relpath)

#     def cycle(self):
#         pass

# class AppEngineOutputChunkedFile(AppEngineOutputFile):
#     def __init__(self,conf_relpath=pathlib.Path):
#         super().__init__(conf_relpath=conf_relpath)

#     def cycle(self):
#         pass