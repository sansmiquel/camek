import sys
import logging
import re
import datetime
import pathlib

class ModuleFilter(logging.Filter):
    def __init__(self,module_name=str):
        super().__init__()
        self.module_name = module_name

    def filter(self, record):
        return record.name == self.module_name

class ModuleMessageFilter(logging.Filter):
    def __init__(self,module_name=str, msg_pattern=str):
        super().__init__()
        self.module_name = module_name
        self.parityfile_regex =   re.compile(msg_pattern)

    def filter(self, record):
        return (record.name == self.module_name) and (self.parityfile_regex.search(record.message))

def get_logger(module_name=None) -> logging.Logger:
    if module_name:
        return logging.getLogger(module_name)
    else:
        return logging.getLogger()

def configure(main_logger=logging.Logger, verbosity_level_console=str, verbosity_level_file=str, log_path=pathlib.Path) -> None:

    main_logger.setLevel(logging.DEBUG)

    now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

    # configurable file logging
    log_filepath = log_path.joinpath(f"{now}_camek.log")
    file_Hdl = logging.FileHandler(log_filepath, mode='w') 
    fmt_file = logging.Formatter(
        "[%(name)s][%(asctime)s][%(levelname)s] %(message)s"
    )
    file_Hdl.setFormatter(fmt_file)

    if verbosity_level_file == 'info':
        file_Hdl.setLevel(logging.INFO) 
    elif verbosity_level_file == 'warning':
        file_Hdl.setLevel(logging.WARNING) 
    elif verbosity_level_file == 'error':
        file_Hdl.setLevel(logging.ERROR) 
    elif verbosity_level_file == 'critical':
        file_Hdl.setLevel(logging.CRITICAL) 
    else:
        file_Hdl.setLevel(logging.DEBUG) 
    main_logger.addHandler(file_Hdl)
    
    # configurable levels console logging
    stdout_StandardHdl = logging.StreamHandler(stream=sys.stdout)
    fmt_console = logging.Formatter(
        "[%(name)s][%(asctime)s][%(levelname)s] %(message)s"
    )
    stdout_StandardHdl.setFormatter(fmt_console)

    if verbosity_level_console == 'info':
        stdout_StandardHdl.setLevel(logging.INFO)
    elif verbosity_level_console == 'warning':
        stdout_StandardHdl.setLevel(logging.WARNING) 
    elif verbosity_level_console == 'error':
        stdout_StandardHdl.setLevel(logging.ERROR)
    elif verbosity_level_console == 'critical':
        stdout_StandardHdl.setLevel(logging.CRITICAL)
    else:
        stdout_StandardHdl.setLevel(logging.DEBUG)
        
    main_logger.addHandler(stdout_StandardHdl)

    return None