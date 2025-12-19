import pathlib
import importlib.util

from camek.exceptions import CamekError as CamekError
import camek.logging as camek_logging
module_logger = camek_logging.get_logger(__name__)
import camek.modules.builtin.io as io

script_path = pathlib.Path(__file__).absolute()
modules_path = script_path.joinpath(script_path.parent,"modules","custom")
topmodules_path = modules_path.joinpath("top")

class AppEngine():
    def __init__(
            self,
            top_module: str,
            topl_conf: pathlib.Path,
            isrc_conf: pathlib.Path,
            osnk_conf: pathlib.Path,
            in_type: str='file',
            out_type: str='file',
            ):
        self.in_type = in_type
        self.out_type = out_type
        try:
            spec = importlib.util.spec_from_file_location(top_module, topmodules_path.joinpath( top_module + ".py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except FileNotFoundError as e:
            module_logger.critical(e)
            raise e
        
        self.conf = {
            'topl': topl_conf.absolute(),  # top-level processor module configuration
            'isrc': isrc_conf.absolute(),  # input source module configuration
            'osnk': osnk_conf.absolute(),  # output sink module configuration
        }
        if self.in_type == 'file':
            self.audioIn = io.AudioFileIn(self.conf['isrc'])
        elif self.in_type == 'chunkedfile':            
            self.audioIn = io.AudioChunkedFileIn(self.conf['isrc'])
        #elif self.in_type == 'device':
        #    pass
        else:
            msg = "Unsupported audio input type."
            module_logger.critical(msg)        
            raise CamekError(msg)                
        if self.out_type == 'file':
            self.audioOut = io.AudioFileOut(self.conf['osnk'])
        elif self.out_type == 'chunkedfile':            
            self.audioOut = io.AudioChunkedFileOut(self.conf['osnk'])
        #elif self.out_type == 'device':
        #    pass
        else:
            msg = "Unsupported audio output type."
            module_logger.critical(msg)        
            raise CamekError(msg)                
        self.topLevelProcessing = module.Top(self.conf['topl'])

    def terminate(self):
        self.audioIn.terminate()
        #self.audioOut.terminate() # FIXME
    
    def run(self):
        pass