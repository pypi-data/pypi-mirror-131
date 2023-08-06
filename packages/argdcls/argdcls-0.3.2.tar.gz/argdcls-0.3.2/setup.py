# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argdcls']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'argdcls',
    'version': '0.3.2',
    'description': 'A simple tool to use dataclass as your config',
    'long_description': "[![ci](https://github.com/sotetsuk/argdcls/actions/workflows/ci.yml/badge.svg)](https://github.com/sotetsuk/argdcls/actions/workflows/ci.yml)\n[![python-version](https://img.shields.io/pypi/pyversions/argdcls)](https://pypi.org/project/argdcls)\n[![pypi](https://img.shields.io/pypi/v/argdcls)](https://pypi.org/project/argdcls)\n\n# Argdcls\n\nA simple tool to use dataclass as your config\n\n## Usage\n\n```py\nfrom dataclasses import dataclass\n\nimport argdcls\n\n\n@dataclass\nclass Config:\n    lr: float\n    adam: bool = False\n\n\nconfig = argdcls.load(Config)\nprint(config)\n```\n\n```sh\n$ python3 main.py @lr=1.0\nConfig(lr=1.0, adam=False)\n$ python3 main.py lr=1.0 adam=True +outdir=results\nConfig(lr=1.0, adam=True, outdir='result')\n```\n\n|| `@param` | `param` | `+param` | `++param` |\n|:---|:---:|:---:|:---:|:---:|\n|w/o default value|OK|OK|Error|OK|\n|w/ default value|Error|OK|Error|OK|\n|not dfined|Error|Error|OK|OK|\n\n## License\nMIT\n",
    'author': 'Sotetsu KOYAMADA',
    'author_email': 'koyamada-s@sys.i.kyoto-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sotetsuk/argdcls',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
