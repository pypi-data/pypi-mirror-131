ユーティリティライブラリ

[![Test](https://github.com/atu4403/adash/actions/workflows/test.yml/badge.svg)](https://github.com/atu4403/adash/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/adash.svg)](https://badge.fury.io/py/adash)

## install

```bash
pip install adash
```

## useit

[Lodash](https://lodash.com/)のような使い方を推奨します。

```python
import adash as _

s = "abcabc"
obj = {"a": "!", "b": "", "c": "?"}
_.replace_all(s, obj) #-> !?!?
```

[adash API documentation](https://atu4403.github.io/adash/adash/)
