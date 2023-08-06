# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['adash']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'adash',
    'version': '0.2.0',
    'description': 'Utility',
    'long_description': 'ユーティリティライブラリ\n\n[![Test](https://github.com/atu4403/adash/actions/workflows/test.yml/badge.svg)](https://github.com/atu4403/adash/actions/workflows/test.yml)\n[![PyPI version](https://badge.fury.io/py/adash.svg)](https://badge.fury.io/py/adash)\n\n## install\n\n```bash\npip install adash\n```\n\n## useit\n\n[Lodash](https://lodash.com/)のような使い方を推奨します。\n\n```python\nimport adash as _\n\ns = "abcabc"\nobj = {"a": "!", "b": "", "c": "?"}\n_.replace_all(s, obj) #-> !?!?\n```\n\n[adash API documentation](https://atu4403.github.io/adash/adash/)\n',
    'author': 'atu4403',
    'author_email': '73111778+atu4403@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/atu4403',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
