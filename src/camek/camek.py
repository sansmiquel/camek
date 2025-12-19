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
        top_module: str,
        topl_conf: str, 
        isrc_conf: str, 
        osnk_conf: str,
        in_type: str='file', 
        out_type: str='file', 
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
    
    
    start_time = time.time()
    from camek.exceptions import CamekError as CamekError
    from camek.appengine import AppEngine as AppEngine
    try:
        app = AppEngine(
            top_module=top_module,
            topl_conf=pathlib.Path(topl_conf),
            isrc_conf=pathlib.Path(isrc_conf),
            osnk_conf=pathlib.Path(osnk_conf),
            in_type=in_type,
            out_type=out_type,
            )
    except CamekError as e:
        msg = f"Processing aborted due to previous error(s): {e}"
        module_logger.critical(msg)
        msg = "camek finished with error(s) in %s seconds." % (time.time() - start_time)
        module_logger.info(msg)
        try:
            app.terminate()
        except CamekError as e_close_file:
            msg = f"Closing audio input/output failed: {e_close_file}"
            module_logger.error(msg)
        raise e

    # run
    try:
        app.run()
    except CamekError as e:
        msg = f"Processing aborted due to previous error(s): {e}"
        module_logger.critical(msg)
        msg = "camek finished with error(s) in %s seconds." % (time.time() - start_time)
        module_logger.info(msg)
        raise e
    
    # terminate & clean-up
    try:
        app.terminate()
    except CamekError as e_close_file:
        msg = f"Closing audio input/output failed: {e_close_file}"
        module_logger.error(msg)
        msg = "camek finished with error(s) in %s seconds." % (time.time() - start_time)
    else:
        msg = "camek finished successfully in %s seconds." % (time.time() - start_time)
    finally:
        module_logger.info(msg)
    
    return None
