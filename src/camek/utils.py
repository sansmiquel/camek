import pathlib
import json

import camek.logging as camek_logging
module_logger = camek_logging.get_logger(__name__)

def read_conf(p: pathlib.Path) -> dict:
        try:
            with open(p, 'r') as f:
                conf = json.load(f)
        except (IOError) as e:
            msg = f"{p}: Unable to read: {e}"
            module_logger.critical(msg)
            raise e # critical error
        except json.JSONDecodeError as e:
            msg = f"{p}: json format error: {e}" 
            module_logger.critical(msg)
            raise e # critical error
        return conf