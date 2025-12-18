import pathlib

from camek.exceptions import CamekError as CamekError
import camek.logging as camek_logging
module_logger = camek_logging.get_logger(__name__)
import camek.appengine.configurator as configurator
#import camek.appengine.io.iofile as iofile
#import camek.appengine.io.iodevice as iodevice

class AppEngine():
    def __init__(self, topl_conf: pathlib.Path, isrc_conf: pathlib.Path, osnk_conf: pathlib.Path):
        self.conf = dict()
        self.conf['configfiles'] = {
            'topl': topl_conf.absolute(),  # top-level processor module configuration
            'isrc': isrc_conf.absolute(),  # input source module configuration
            'osnk': osnk_conf.absolute(),  # output sink module configuration
        }
        self.conf['moduleconfig'] = {}
        
        for k in self.conf['configfiles'].keys():
            self.conf['moduleconfig'][k] = configurator.get_conf(self.conf['configfiles'][k])

        self.conf['app'] = {}
        configurator.get_submodules_conf(
            conf=self.conf['app'],
            submodules_list=self.conf['moduleconfig']['topl']['_submodules'],
            conf_relpath=self.conf['moduleconfig']['topl']['_conf_relpath'])
        pass
        # if self.conf['moduleconfig']['isrc']['type'] == 'file':
        #     self.audio_in = iofile.AppEngineInputEntireFile(self.conf['moduleconfig'])
        # elif self.conf['isrc']['type'] == 'chunkedfile':
        #     self.audio_in = iofile.AppEngineInputChunkedFile(self.conf['moduleconfig'])
        # #elif self.conf['isrc']['type'] == 'device':
        # #    self.audio_in = iofile.AppEngineInputDevice(self.conf['moduleconfig'])
        # else:
        #     # critical error
        #     msg = f"Unexpected input source type: {self.conf['moduleconfig']['isrc']['type']}"
        #     module_logger.critical(msg)
        #     raise CamekError(msg)

        # if self.conf['osnk']['type'] == 'file':
        #     self.audio_out = iofile.AppEngineOutputEntireFile(self.conf['osnk'])
        # elif self.conf['osnk']['type'] == 'chunkedfile':
        #     self.audio_out = iofile.AppEngineOutputChunkedFile(self.conf['osnk'])
        # #elif self.conf['osnk']['type'] == 'device':
        # #    self.audio_out = iofile.AppEngineOutputDevice(self.conf['osnk'])
        # else:
        #     # critical error
        #     msg = f"Unexpected output sink type: {self.conf['osnk']['type']}"
        #     module_logger.critical(msg)
        #     raise CamekError(msg)