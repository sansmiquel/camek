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
       self.direction = None  # ['input', 'output']
       self.type = None  # ['file', 'chunkedfile','device']

    @abstractmethod
    def get_status(self):
        pass
    @abstractmethod
    def cycle(self):
        pass
    @abstractmethod
    def terminate(self):
        pass

class AudioFileIo(AudioIo):

    def __init__(self,conf_relpath=pathlib.Path):
        super().__init__(conf_relpath=conf_relpath)  
        self.nchan = self.conf["nchan"]
        self.nchan = self.conf["nchan"]
        self._get_files()

    def _close_files(self):
        [f.close for f in self.fptr]
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
    
    def _check_metadata(self) -> None:
        nchan_err = False
        sr_err = False
        nsamples_err = False
        for k, elem in enumerate(self.metadata[1:]):
            if elem['nchan'] != self.metadata[k-1]['nchan']:
                nchan_err = True
                msg = f"Mismatch, channels number: {self.files_list[k-1]} : {self.metadata[k-1]['nchan']},  {self.files_list[k]} : {elem['nchan']}"
                module_logger.error(msg)
            if elem['sr'] != self.metadata[k-1]['sr']:
                sr_err = True
                msg = f"Mismatch, sample rate: {self.files_list[k-1]} : {self.metadata[k-1]['sr']},  {self.files_list[k]} : {elem['sr']}"
                module_logger.error(msg)
            if elem['nsamples'] != self.metadata[k-1]['nsamples']:
                nsamples_err = True
                msg = f"Mismatch, sampless number: {self.files_list[k-1]} : {self.metadata[k-1]['nsamples']},  {self.files_list[k]} : {elem['nsamples']}"
                module_logger.error(msg)
        if nchan_err or sr_err or nsamples_err:
            msg = f"Metadata mismatch ({self.direction}) files: chan nb: {nchan_err},  samples nb: {nsamples_err},  sample rate num: {sr_err}. "
            module_logger.critical(msg)
            self._close_files()
            raise CamekError(msg)
        
    def terminate(self):
        self._close_files()

    @abstractmethod
    def _init_src(self):
        pass
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
        self._init_src()   

    def _init_src(self):
        self.fptr = list()
        self.metadata = list()
        for p in self.files_list:
            f = sf.SoundFile(str(p),'r')
            self.metadata.append({'sr': f.samplerate, 'nsamples': f.frames, 'nchan': f.channels})
            self.fptr.append(f)
        self._check_metadata()

    def get_status(self):
        pass
    def cycle(self):
        pass

class AudioChunkedFileIn(AudioFileIo):
    def __init__(self,conf_relpath=pathlib.Path):
        super().__init__(conf_relpath=conf_relpath)  
        if self.conf['type'] != 'file':
            msg = f"Invalid audio input module configuration: Expected type 'chunkedfile', got {self.conf['type']}"
            module_logger.critical(msg)        
            raise CamekError(msg)   
    def _init_src(self):
        pass
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
    def _init_src(self):
        pass
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
    def _init_src(self):
        pass
    def get_status(self):
        pass
    def cycle(self):
        pass
