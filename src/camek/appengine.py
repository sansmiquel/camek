import pathlib
import importlib.util

from camek.exceptions import CamekError as CamekError
import camek.logging as camek_logging
module_logger = camek_logging.get_logger(__name__)
import camek.modules.builtin.io as io

script_path = pathlib.Path(__file__).absolute()
modules_path = script_path.joinpath(script_path.parent.parent,"modules","custom")
topmodules_path = modules_path.joinpath("top")

class AppEngine():
    def __init__(self, top_module: str, topl_conf: pathlib.Path, isrc_conf: pathlib.Path, osnk_conf: pathlib.Path):
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

        self.audioIn = io.AudioInput(self.conf['isrc'])
        self.audioOut = io.AudioOutput(self.conf['osnk'])
        self.topLevelProcessing = module.Top(self.conf['topl'])

    def run(self):
        pass