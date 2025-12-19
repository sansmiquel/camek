from abc import ABC, abstractmethod
import camek.utils as utils
import pathlib

class Module(ABC):
    def __init__(self,conf_relpath: pathlib.Path):
        self.conf = utils.read_conf(p=conf_relpath.resolve())

    @abstractmethod
    def cycle(self) -> None:
        pass

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
    def cycle(self) -> None:
        pass