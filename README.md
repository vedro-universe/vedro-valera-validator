# Vedro Valera Validator

[![Codecov](https://img.shields.io/codecov/c/github/nikitanovosibirsk/vedro-valera-validator/master.svg?style=flat-square)](https://codecov.io/gh/nikitanovosibirsk/vedro-valera-validator)
[![PyPI](https://img.shields.io/pypi/v/vedro-valera-validator.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-valera-validator/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/vedro-valera-validator?style=flat-square)](https://pypi.python.org/pypi/vedro-valera-validator/)
[![Python Version](https://img.shields.io/pypi/pyversions/vedro-valera-validator.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-valera-validator/)

## Installation

### 1. Install package

```shell
$ pip3 install vedro-valera-validator
```

### 2. Enable plugin

```python
# ./vedro.cfg.py
import vedro
import vedro_valera_validator as v


class Config(vedro.Config):

    class Plugins(vedro.Config.Plugins):

        class ValeraValidator(v.ValeraValidator):
            enabled = True
```

## Usage

### Run tests

```shell
$ vedro run
```
