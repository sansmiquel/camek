import pathlib

from camek.exceptions import CamekError as CamekError
import camek.appengine.configurator.configurator as configurator
import camek.appengine.io.iofile as iofile
#import camek.appengine.io.iodevice as iodevice

class AppEngine():
    def __init__(self, proc_conf: pathlib.Path, isrc_conf: pathlib.Path, osnk_conf: pathlib.Path):
        self.conf = dict()
        self.conf_paths = {
            'proc': proc_conf.absolute(),  # processor configuration
            'isrc': isrc_conf.absolute(),  # input source configuration
            'osnk': osnk_conf.absolute(),  # output sink configuration
        }
        proc_configurator = configurator.ProcessingConfigurator(self.conf_paths['proc'])
        self.conf['proc'] = proc_configurator.get()
        
        for k in {'isrc','osnk'}:
            io_configurator = configurator.IOConfigurator(self.conf_paths[k])
            self.conf[k] = io_configurator.get()
        #
        if self.conf['isrc']['type'] == 'file':
            self.audio_in = iofile.AppEngineInputEntireFile(self.conf['isrc'])
        elif self.conf['isrc']['type'] == 'chunkedfile':
            self.audio_in = iofile.AppEngineInputChunkedFile(self.conf['isrc'])
        #elif self.conf['isrc']['type'] == 'device':
        #    self.audio_in = iofile.AppEngineInputDevice(self.conf['isrc'])
        else:
            # critical error
            raise CamekError(f"Unexpected input source type: {self.conf['isrc']['type']}")

        if self.conf['osnk']['type'] == 'file':
            self.audio_out = iofile.AppEngineOutputEntireFile(self.conf['osnk'])
        elif self.conf['osnk']['type'] == 'chunkedfile':
            self.audio_out = iofile.AppEngineOutputChunkedFile(self.conf['osnk'])
        #elif self.conf['osnk']['type'] == 'device':
        #    self.audio_out = iofile.AppEngineOutputDevice(self.conf['osnk'])
        else:
            # critical error
            raise CamekError(f"Unexpected output sink type: {self.conf['osnk']['type']}")
        