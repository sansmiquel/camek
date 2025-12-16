import pathlib
import tomli

def read_conf(p: pathlib.Path) -> dict:
        try:
            with open(p, 'rb') as f:
                conf = tomli.load(f)
        except (IOError, tomli.TOMLDecodeError) as err:
            print(f"ERROR: could not read config file {p}: ", err)
            raise err # critical error
        return conf

class ProcessingConfigurator():
    
    def __init__(self, p=pathlib.Path):
        self.conf = dict()
        filecontent = read_conf(p)
        self.conf_path = pathlib.Path(p.parent,*filecontent['conf_relpath']).resolve()
        self._walk(filecontent=filecontent, cfg=self.conf)

    def _walk(self, filecontent= dict, cfg= dict) -> None:
        for key, item in filecontent.items():
            if isinstance(item,dict):
                k = '_sub_' + key
                cfg[k] = dict()
                self._walk(item,cfg[k])
            elif key == '_conf' and isinstance(item, str): # sub-module conf file
                path_parts=list(self.conf_path.parts)
                path_parts.append(item)
                self._get_conf(path_parts=path_parts, cfg=cfg)
            else:
                cfg[key] = item  # key,value parametrization

        return None

    def _get_conf(self, path_parts=list, cfg=dict) -> None:
        filecontent = read_conf(pathlib.Path(*path_parts))
        self._walk(filecontent=filecontent, cfg=cfg)
        return None

    def get(self) -> dict:
        return self.conf

class IOConfigurator():
    
    def __init__(self, p=pathlib.Path, sampling_rate=float, frame_len=int):
        self.conf = read_conf(p)
        #self.conf['sampling_rate'] = self.conf['proc']['sampling_rate']
        #self.conf['frame_len'] = self.conf['proc']['frame_len']

        self.conf_path = pathlib.Path(p.parent,*self.conf['conf_relpath']).resolve()

    def get(self) -> dict:
        return self.conf
