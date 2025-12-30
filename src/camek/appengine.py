from camek.exceptions import CamekError as CamekError
import camek.logging as camek_logging
module_logger = camek_logging.get_logger(__name__)
import camek.modules.builtin as camek_modules
import pathlib
import importlib.util

script_path = pathlib.Path(__file__).absolute()
topmodules_path = script_path.joinpath(script_path.parent,"modules","top")

class AppEngine():
    def __init__(
            self,
            top_module: str,
            topl_conf: str,
            isrc_conf: str,
            osnk_conf: str,
            in_type: str='file',
            out_type: str='file',
            ):
        self.in_type = in_type
        self.out_type = out_type
        try:
            spec = importlib.util.spec_from_file_location(top_module, topmodules_path.joinpath( top_module, top_module + ".py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except FileNotFoundError as e:
            module_logger.critical(e)
            raise e

        # top level processing module
        self.topLevelProcessing = module.TopLevelProcessingModule(conf_relpath=[topl_conf])

        # top level audio input source module
        nchan, sr, frame_len, data_type = self.topLevelProcessing.get_formats_in()
        if self.in_type == 'file':
            self.audioIn = camek_modules.AudioFileIn(
                conf_relpath=[isrc_conf],
                nchan=nchan,
                sr=sr,
                frame_len=frame_len,
                data_type=data_type,
                )
        #elif self.in_type == 'device':
        #    pass
        else:
            msg = "Unsupported audio input type."
            module_logger.critical(msg)        
            raise CamekError(msg)           
             
        # top level audio output sink module
        nchan, sr, frame_len, data_type = self.topLevelProcessing.get_formats_out()
        if self.out_type == 'file':
            self.audioOut = camek_modules.AudioFileOut(
                conf_relpath=[osnk_conf],
                nchan=nchan,
                sr=sr,
                frame_len=frame_len,
                data_type=data_type,
                )
        #elif self.out_type == 'device':
        #    pass
        else:
            msg = "Unsupported audio output type."
            module_logger.critical(msg)        
            raise CamekError(msg)                

    def terminate(self):
        self.audioIn.terminate()
        self.audioOut.terminate()
    
    def run(self):
        process_data = True
        while(process_data):

            # top-level input source module
            self.audioIn.cycle()
            x = self.audioIn.get_output()
            audioin_status, sample_idx, frame_idx = self.audioIn.get_status()
            process_data = process_data and audioin_status
            #print(f"{frame_idx} {sample_idx} {process_data} {self.audioIn.nsamples}")

            # top-level processing module
            self.topLevelProcessing.cycle(input=x)
            x = self.topLevelProcessing.get_output()
            topl_status = self.topLevelProcessing.get_status()
            process_data = process_data and topl_status

            # top-level output sink module
            self.audioOut.cycle(input=x)
            audioout_status, sample_idx, frame_idx = self.audioOut.get_status()
            process_data = process_data and audioout_status
            #print(f"{frame_idx} {sample_idx} {process_data}")

        