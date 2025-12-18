### Custom Audio Modules Engine Kit (camek) main module

## Import
import sys
import pathlib
import datetime
import time

## paths
userconfig = pathlib.Path.home().joinpath('.config','camek')  # workspace path
workspace = pathlib.Path.home().joinpath('.camek')  # workspace path

## logging
import camek.logging as camek_logging
log_path = workspace.joinpath(workspace,'log')
main_logger = camek_logging.get_logger()
module_logger = camek_logging.get_logger(__name__)

# -------------------------------------------------------------------------
def main(
        topl_conf: str, 
        isrc_conf: str, 
        osnk_conf: str, 
        verbosity_level_console: str='warning',
        verbosity_level_file: str='info',
        ) -> None:
    """Main function for camek application."""
    try:
        log_path.mkdir(parents=True,exist_ok=True)
    except FileExistsError as e:
        msg = f"{log_path}: cannot be used for logging: {e}"
        print(msg)
        return 1    
    
    camek_logging.configure(
        main_logger=main_logger,
        verbosity_level_console=verbosity_level_console,
        verbosity_level_file=verbosity_level_file,
        log_path=log_path,
        )
    
    msg = "Processing aborted due to previous error(s)."
    start_time = time.time()
    from camek.exceptions import CamekError as CamekError
    from camek.appengine.appengine import AppEngine as AppEngine
    try:
        AppEngine(
            topl_conf=pathlib.Path(topl_conf),
            isrc_conf=pathlib.Path(isrc_conf),
            osnk_conf=pathlib.Path(osnk_conf),
            )
    except CamekError as e:
        module_logger.critical(msg)
        msg = "audioprocessor finished with error(s) in %s seconds." % (time.time() - start_time)
        module_logger.info(msg)
        raise e

    msg = "camek finished successfully in %s seconds." % (time.time() - start_time)
    module_logger.info(msg)
    
    return None
