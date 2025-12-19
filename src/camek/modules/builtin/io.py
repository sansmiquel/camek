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
    def __init__(self,conf_relpath: pathlib.Path):
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

    def __init__(self,conf_relpath: pathlib.Path, nchan: int, sr: int):
        super().__init__(conf_relpath=conf_relpath)  
        self.nchan = nchan
        self.sr = sr
        if self.nchan != self.conf["nchan"]:
            msg = f"Channel number configuration mismatch: top-level module conf: {self.nchan}, audio module conf: {self.conf["nchan"]}"
            raise CamekError(msg)
        self.conf_relpath = self.conf["conf_relpath"]
        self.conf_stem = self.conf["conf_stem"]
        self.conf_suffix = self.conf["conf_suffix"]
        self.file_prefix = self.conf["file_prefix"]
        self.file_format = self.conf["file_format"]
        self.subtype = self.conf["subtype"]
        self.fptr = list()
        self.metadata = list()
        self._get_files()

    def _close_files(self):
        [f.close for f in self.fptr]

    def _get_files(self) -> None:
        p = pathlib.Path(
            *self.conf_relpath,
            self.conf_stem+self.conf_suffix).resolve()
        conf = utils.read_conf(p)
        self.files_list = []
        for k in range(0,self.nchan):
            self.files_list.append(
                pathlib.Path(*conf['path'],self.file_prefix + f"{k}." + self.file_format))
        return None
    
    def _check_metadata(self) -> None:
        sr_err = False
        nsamples_err = False
        for k, elem in enumerate(self.metadata[1:]):
            if elem['sr'] != self.sr :
                sr_err = True
                msg = f"Mismatch, sample rate: file {self.files_list[k-1]} : {self.metadata[k-1]['sr']},  top-level module conf: {elem['sr']}"
                module_logger.error(msg)
            if elem['nsamples'] != self.metadata[k-1]['nsamples']:
                nsamples_err = True
                msg = f"Mismatch, sampless number: file {self.files_list[k-1]} : {self.metadata[k-1]['nsamples']},  file {self.files_list[k]} : {elem['nsamples']}"
                module_logger.error(msg)
        if sr_err or nsamples_err:
            msg = f"Metadata mismatch ({self.direction}) files: samples nb: {nsamples_err},  sample rate num: {sr_err}. "
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
    def __init__(self,conf_relpath: pathlib.Path, nchan: int, sr: int):
        super().__init__(conf_relpath=conf_relpath, nchan=nchan, sr=sr)  
        if self.conf['type'] != 'file':
            msg = f"Invalid audio input module configuration: Expected type 'file', got {self.conf['type']}"
            module_logger.critical(msg)        
            raise CamekError(msg)
        self.type = 'file'
        self.direction = 'input'
        self._init_src()   

    def _init_src(self):
        for p in self.files_list:
            f = sf.SoundFile(str(p),'r')
            if f.channels != 1:
                msg = f"Ambiguity found: more than 1 channel found in file: {p}"
                module_logger.critical(msg)        
                self._close_files()
                raise CamekError(msg)
            self.metadata.append({'sr': f.samplerate, 'nsamples': f.frames})
            self.fptr.append(f)
        self._check_metadata()
        self.nsamples = self.metadata[0]['nsamples'] 

    def get_status(self):
        pass
    def cycle(self):
        pass

class AudioChunkedFileIn(AudioFileIo):
    def __init__(self,conf_relpath: pathlib.Path, nchan: int, sr: int):
        super().__init__(conf_relpath=conf_relpath, nchan=nchan, sr=sr)   
        if self.conf['type'] != 'chunkedfile':
            msg = f"Invalid audio input module configuration: Expected type 'chunkedfile', got {self.conf['type']}"
            module_logger.critical(msg)        
            raise CamekError(msg)
        self.type = 'chunkedfile'
        self.direction = 'input'   
    def _init_src(self):
        pass
    def get_status(self):
        pass
    def cycle(self):
        pass

class AudioFileOut(AudioFileIo):
    def __init__(self,conf_relpath: pathlib.Path, nchan: int, sr: int):
        super().__init__(conf_relpath=conf_relpath, nchan=nchan, sr=sr)
        if self.conf['type'] != 'file':
            msg = f"Invalid audio input module configuration: Expected type 'file', got {self.conf['type']}"
            module_logger.critical(msg)        
            raise CamekError(msg)
        self.type = 'file'
        self.direction = 'output'   
    def _init_src(self):
        for p in self.files_list:
            f = sf.SoundFile(
                str(p),
                'w',
                channels=1,
                samplerate=self.sr,
                subtype=self.subtype,
                )
            self.fptr.append(f)
    def get_status(self):
        pass
    def cycle(self):
        pass

class AudioChunkedFileOut(AudioFileIo):
    def __init__(self,conf_relpath: pathlib.Path, nchan: int, sr: int):
        super().__init__(conf_relpath=conf_relpath, nchan=nchan, sr=sr)   
        if self.conf['type'] != 'file':
            msg = f"Invalid audio input module configuration: Expected type 'chunkedfile', got {self.conf['type']}"
            module_logger.critical(msg)        
            raise CamekError(msg)
        self.type = 'chunkedfile'
        self.direction = 'output'      
    def _init_src(self):
        pass
    def get_status(self):
        pass
    def cycle(self):
        pass
