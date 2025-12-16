### Custom Audio Modules Engine Kit (camek) main module

## Import
import sys
import pathlib
import datetime
import time

## paths
userconfig = pathlib.Path.home().joinpath('.config','camek')  # workspace path
workspace = pathlib.Path.home().joinpath('.camek')  # workspace path

# Exceptions
from camek.exceptions import CamekError as CamekError

## logging
#import camek.logging as camek_logging
log_path = workspace.joinpath(workspace,'log')
#main_logger = camek_logging.get_logger()
#module_logger = camek_logging.get_logger(__name__)

# -------------------------------------------------------------------------
# main 

# def main(
#         aproc_conf: str, 
#         isrc_conf: str, 
#         osnk_conf_: str, 
#         verbosity_level: str='warning',
#         ) -> None:
def main() -> None:

    start_time = time.time()

    # try:
    #     log_path.mkdir(parents=True,exist_ok=True)
    # except FileExistsError as e:
    #     msg = f"{log_path}: cannot be used for logging: {e}"
    #     print(msg)
    #     return 1    
    
    #camek_logging.configure(main_logger=main_logger, verbosity_level=verbosity_level, log_path=log_path)
  
    msg = "Processing aborted due to previous error(s)."
    
    # FIXME

    msg = "camek finished successfully in %s seconds." % (time.time() - start_time)
    #module_logger.info(msg)
    
    return None
