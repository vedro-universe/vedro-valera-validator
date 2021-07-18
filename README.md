# Vedro Valera Validator

[![PyPI](https://img.shields.io/pypi/v/vedro-valera-validator.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-valera-validator/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/vedro-valera-validator?style=flat-square)](https://pypi.python.org/pypi/vedro-valera-validator/)
[![Python Version](https://img.shields.io/pypi/pyversions/vedro-valera-validator.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-valera-validator/)

## Installation

```shell
$ pip3 install vedro-valera-validator
```

```python
# ./bootstrap.py
import vedro
from vedro_valera_validator import ValeraValidator

vedro.run(plugins=[ValeraValidator()])
```

## Usage

### Run tests

```shell
$ python3 bootstrap.py -vv
```
