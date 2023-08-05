# py-az-cli
Pythonic wrapper for az cli

Requires Python 3

## Install 
Note: We recommend first creating a virtual env and activating it
```
pip install py-az-cli
```

## Usage
```
% python3
>>> import pyaz
>>> result = pyaz.version()
>>> print(result)
{'azure-cli': '2.28.1', 'azure-cli-core': '2.28.1', 'azure-cli-telemetry': '1.0.6', 'extensions': {}}
```
