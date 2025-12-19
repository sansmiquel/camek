from abc import abstractmethod
from camek.modules.module import Module
from camek.exceptions import CamekError as CamekError
import camek.utils as utils
import camek.logging as camek_logging
module_logger = camek_logging.get_logger(__name__)
import pathlib
import json
import math
import numpy as np
import soundfile as sf

class AudioIo(Module):
    def __init__(self,conf_relpath=pathlib.Path):
       super().__init__(conf_relpath=conf_relpath)

    @abstractmethod
    def get_status(self):
        pass
    @abstractmethod
    def cycle(self):
        pass

class AudioFileIo(AudioIo):

    def __init__(self,conf_relpath=pathlib.Path):
        super().__init__(conf_relpath=conf_relpath)  
        self.nchan = self.conf["nchan"]
        self._get_files()

    def _get_files(self) -> None:
        p = pathlib.Path(
            *self.conf["conf_relpath"],
            self.conf["conf_stem"]+self.conf["conf_suffix"]).resolve()
        conf = utils.read_conf(p)
        self.files_list = []
        for k in range(0,self.nchan):
            self.files_list.append(
                pathlib.Path(*conf['path'],self.conf["file_prefix"] + f"{k}." + self.conf["file_format"]))
        return None
    
    @abstractmethod
    def get_status(self):
        pass
    @abstractmethod
    def cycle(self):
        pass

class AudioFileIn(AudioFileIo):
    def __init__(self,conf_relpath=pathlib.Path):
        super().__init__(conf_relpath=conf_relpath)  
        if self.conf['type'] != 'file':
            msg = f"Invalid audio input module configuration: Expected type 'file', got {self.conf['type']}"
            module_logger.critical(msg)        
            raise CamekError(msg)   
        
    def get_status(self):
        passs
    def cycle(self):
        pass

class AudioChunkedFileIn(AudioFileIo):
    def __init__(self,conf_relpath=pathlib.Path):
        super().__init__(conf_relpath=conf_relpath)  
        if self.conf['type'] != 'file':
            msg = f"Invalid audio input module configuration: Expected type 'chunkedfile', got {self.conf['type']}"
            module_logger.critical(msg)        
            raise CamekError(msg)   
    def get_status(self):
        pass
    def cycle(self):
        pass

class AudioFileOut(AudioFileIo):
    def __init__(self,conf_relpath=pathlib.Path):
        super().__init__(conf_relpath=conf_relpath)  
        if self.conf['type'] != 'file':
            msg = f"Invalid audio input module configuration: Expected type 'file', got {self.conf['type']}"
            module_logger.critical(msg)        
            raise CamekError(msg)   
    def get_status(self):
        pass
    def cycle(self):
        pass

class AudioChunkedFileOut(AudioFileIo):
    def __init__(self,conf_relpath=pathlib.Path):
        super().__init__(conf_relpath=conf_relpath)  
        if self.conf['type'] != 'file':
            msg = f"Invalid audio input module configuration: Expected type 'chunkedfile', got {self.conf['type']}"
            module_logger.critical(msg)        
            raise CamekError(msg)   
    def get_status(self):
        pass
    def cycle(self):
        pass
