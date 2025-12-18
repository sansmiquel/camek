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
    def _get_files(self,
                   conf_relpath=list,
                   conf_stem=str,
                   conf_suffix=str,
                   nchan=int,
                   file_prefix=str,
                   file_format=str,
                   ) -> list:
        p = pathlib.Path(*conf_relpath,conf_stem+conf_suffix).resolve()
        conf = utils.read_conf(p)
        files_list = []
        for k in range(0,nchan):
            files_list.append(pathlib.Path(*conf['path'],file_prefix + f"{k}." + file_format))
        return files_list

    def __init__(self,conf_relpath=pathlib.Path):
        super().__init__(conf_relpath=conf_relpath)  
        self.files_list = self._get_files(
            conf_relpath=self.conf["conf_relpath"],
            conf_stem=self.conf["conf_stem"],
            conf_suffix=self.conf["conf_suffix"],
            nchan=self.conf["nchan"],
            file_prefix=self.conf["file_prefix"],
            file_format=self.conf["file_format"],
        )
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
