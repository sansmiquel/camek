# CustomAudioModulesEngineKit

`camek` (for Custom Audio Modules Engine Kit) is an engine kit that provides a framework to develop, test and run audio processing applications based on customizable modules.

## Disclaimer

`camek` is currently in early development stages and not suited for usage in production.

## License

`camek` is licenced under [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html#license-text)

## How it works

FIXME

## Installation

`camek` is not yet available on `pypi`.

It can be build from source and installed in a dedicated environment as follows:

```bash
pyenv install <python-version>
$HOME/.pyenv/versions/<python-version>/bin/python -m venv $HOME/venv/camek_python<python-version>
source HOME/venv/camek_python<python-version>/bin/activate
pip install build
git clone https://github.com/sansmiquel/camek
cd camek
python -m build
pip install dist/camek-<version>-none-any-whl
```

## Usage

FIXME
