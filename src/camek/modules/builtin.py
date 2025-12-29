from abc import ABC, abstractmethod
from camek.exceptions import CamekError as CamekError
import camek.logging as camek_logging
module_logger = camek_logging.get_logger(__name__)
import camek.utils as utils
import pathlib
import math
import numpy as np
import soundfile as sf

class Module(ABC):
    def __init__(self,conf_relpath: pathlib.Path):
        self.conf = utils.read_conf(p=conf_relpath.resolve())

    @abstractmethod
    def get_status(self) -> None:
        pass
    @abstractmethod
    def cycle(self) -> None:
        pass

class AudioIo(Module):
    def __init__(self,conf_relpath: pathlib.Path):
       super().__init__(conf_relpath=conf_relpath)
       self.direction = None  # ['input', 'output']
       self.type = None  # ['file', 'device']

    def _close_files(self):
        [f.close for f in self.fptr]

    @abstractmethod
    def get_status(self):
        pass
    @abstractmethod
    def get_output(self):
        pass
    @abstractmethod
    def cycle(self):
        pass
    def terminate(self):
        self._close_files()

class AudioFileIo(AudioIo):

    def __init__(self,conf_relpath: pathlib.Path, nchan: int, sr: int, frame_len: int, data_type: str='float64'):
        super().__init__(conf_relpath=conf_relpath)  
        self.nchan = nchan
        self.sr = sr
        self.frame_len = frame_len
        self.dtype = data_type
        if self.nchan != self.conf["nchan"]:
            msg = f"Channel number configuration mismatch: top-level module conf: {self.nchan}, audio module conf: {self.conf["nchan"]}"
            raise CamekError(msg)
        self.conf_relpath = self.conf["conf_relpath"]
        self.conf_stem = self.conf["conf_stem"]
        self.conf_suffix = self.conf["conf_suffix"]
        self.file_prefix = self.conf["file_prefix"]
        self.file_format = self.conf["file_format"]
        self.fptr = list()
        self.metadata = list()
        self._get_files()
        self.frame = np.zeros([self.nchan,self.frame_len])  # FIXME: type should be specified

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
        
    @abstractmethod
    def _init_src(self):
        pass
    @abstractmethod
    def get_output(self):
        pass
    @abstractmethod
    def get_status(self):
        pass
    @abstractmethod
    def cycle(self):
        pass

class AudioFileIn(AudioFileIo):
    def __init__(self,conf_relpath: pathlib.Path, nchan: int, sr: int, frame_len: int, data_type: str='float64'):
        super().__init__(conf_relpath=conf_relpath, nchan=nchan, sr=sr, frame_len=frame_len, data_type=data_type)  
        if self.conf['type'] != 'file':
            msg = f"Invalid audio input module configuration: Expected type 'file', got {self.conf['type']}"
            module_logger.critical(msg)        
            raise CamekError(msg)
        self.type = 'file'
        self.direction = 'input'
        self.sample_idx = -self.frame_len
        self.frame_idx = -1
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
        self.nsamples = math.floor(self.metadata[0]['nsamples'] / self.frame_len) * self.frame_len

    def get_status(self) -> tuple[bool, int, int]:
        return (
            self.sample_idx + self.frame_len < self.nsamples,
            self.sample_idx,
            self.frame_idx,
        )
    def get_output(self) -> np.array:
        return self.frame
    def cycle(self) -> None:
        self.sample_idx += self.frame_len
        self.frame_idx +=1
        for k in range(0,self.nchan):
            self.frame[k,:] = self.fptr[k].read(
                frames=self.frame_len,
                dtype=self.dtype,
                always_2d=False,
                fill_value=None,
                out=None
            )
        return None

class AudioFileOut(AudioFileIo):
    def __init__(self,conf_relpath: pathlib.Path, nchan: int, sr: int, frame_len: int, data_type: str='float64'):
        super().__init__(conf_relpath=conf_relpath, nchan=nchan, sr=sr, frame_len=frame_len, data_type=data_type)
        if self.conf['type'] != 'file':
            msg = f"Invalid audio input module configuration: Expected type 'file', got {self.conf['type']}"
            module_logger.critical(msg)        
            raise CamekError(msg)
        self.type = 'file'
        self.direction = 'output'
        self.sample_idx = -self.frame_len
        self.frame_idx = -1 
        self.subtype = self.conf["subtype"]
        self._init_src()    

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

    def get_status(self) -> tuple[bool, int, int]:
        return (
            True,
            self.sample_idx,
            self.frame_idx,
        )
    
    def get_output(self):
        pass

    def cycle(self, input: np.array):
        self.sample_idx += self.frame_len
        self.frame_idx +=1
        self.frame = input
        for k in range(0,self.nchan):
            self.fptr[k].write(self.frame[k,:])
        return None

class TopModule(Module):
    def __init__(self,conf_relpath: pathlib.Path):
        self.conf = utils.read_conf(p=conf_relpath.resolve())
        self.nchan_in = self.conf["nchan_in"]
        self.nchan_out = self.conf["nchan_out"]
        self.sr_in = self.conf["sample_rate_in"]
        self.sr_out = self.conf["sample_rate_out"]
        self.dtype = self.conf["dtype"]
        self.frame_len = self.conf["frame_len"]

    def get_formats_in(self) -> tuple:
        return (self.nchan_in, self.sr_in, self.frame_len, self.dtype)
    def get_formats_out(self) -> tuple:
        return (self.nchan_in, self.sr_in, self.frame_len, self.dtype)

    @abstractmethod
    def get_status(self) -> None:
        pass
    @abstractmethod
    def get_output(self) -> None:
        pass
    @abstractmethod
    def cycle(self) -> None:
        pass

    class SubModule(Module):
        def __init__(self,conf_relpath: pathlib.Path):
            self.conf = utils.read_conf(p=conf_relpath.resolve())
            self.nchan_in = self.conf["nchan_in"]
            self.nchan_out = self.conf["nchan_out"]
            self.dtype = self.conf["dtype"]
            self.frame_len = self.conf["frame_len"]

        def get_formats_in(self) -> tuple:
            return (self.nchan_in, self.sr_in, self.frame_len, self.dtype)
        def get_formats_out(self) -> tuple:
            return (self.nchan_in, self.sr_in, self.frame_len, self.dtype)

        @abstractmethod
        def get_status(self) -> None:
            pass
        @abstractmethod
        def get_output(self) -> None:
            pass
        @abstractmethod
        def cycle(self) -> None:
            pass