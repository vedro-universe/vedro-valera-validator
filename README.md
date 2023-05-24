# Vedro Valera Validator

[![Codecov](https://img.shields.io/codecov/c/github/vedro-universe/vedro-valera-validator/master.svg?style=flat-square)](https://codecov.io/gh/vedro-universe/vedro-valera-validator)
[![PyPI](https://img.shields.io/pypi/v/vedro-valera-validator.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-valera-validator/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/vedro-valera-validator?style=flat-square)](https://pypi.python.org/pypi/vedro-valera-validator/)
[![Python Version](https://img.shields.io/pypi/pyversions/vedro-valera-validator.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-valera-validator/)

Validator plugin for the [Vedro](https://vedro.io) testing framework.

## How to Install

<details open>
<summary>Quick</summary>
<p>

For a quick installation, you can use a plugin manager like so:

```shell
$ vedro plugin install vedro-valera-validator
```

</p>
</details>

<details>
<summary>Manual</summary>
<p>

To install manually, follow these steps:

1. Install the package using pip:

```shell
$ pip3 install vedro-valera-validator
```

2. Then, enable the plugin in the `vedro.cfg.py` configuration file:

```python
# ./vedro.cfg.py
import vedro
import vedro_valera_validator

class Config(vedro.Config):

    class Plugins(vedro.Config.Plugins):

        class ValeraValidator(vedro_valera_validator.ValeraValidator):
            enabled = True
```

</p>
</details>

## How to Use

Here is an example scenario demonstrating how to decode a base64 encoded string:

```python
# ./scenarios/decode_base64_encoded_string.py
import vedro
from base64 import b64decode
from d42 import schema

class Scenario(vedro.Scenario):
    subject = "decode base64 encoded string"

    def given(self):
        self.encoded = "Y3VjdW1iZXI="

    def when(self):
        self.result = {
            "result": b64decode(self.encoded)
        }

    def then(self):
        assert self.result == schema.dict({
            "result": schema.bytes(b"banana")
        })
```

Run the test using the command:

```shell
$ vedro run -vv
```

If the expected and actual results do not match, a `ValidationException` will be thrown, as shown below:

```shell
ValidationException:
 - Value <class 'bytes'> at _['result'] must be equal to b'banana', but b'cucumber' given
 ```

## Further Reading

For comprehensive guidance and more information, refer to the [official documentation](https://vedro.io/en/docs/integrations/valera-validator).
