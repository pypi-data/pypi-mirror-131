# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['morecopy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'morecopy',
    'version': '0.2.4',
    'description': 'Copy even immutable objects as much as possible',
    'long_description': '# morecopy\n\n[![PyPI](https://img.shields.io/pypi/v/morecopy.svg?label=PyPI&style=flat-square)](https://pypi.org/project/morecopy/)\n[![Python](https://img.shields.io/pypi/pyversions/morecopy.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/project/morecopy/)\n[![Test](https://img.shields.io/github/workflow/status/astropenguin/morecopy/Tests?logo=github&label=Test&style=flat-square)](https://github.com/astropenguin/morecopy/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.5594444-blue?style=flat-square)](https://doi.org/10.5281/zenodo.5594444)\n\nCopy even immutable objects as much as possible\n\n## Overview\n\nmorecopy is a Python package that enables copy of immutable objects so that a copied object is equivalent but not identical to the original:\n\n```python\nfrom morecopy import copy\n\n\noriginal = 1234567890\ncopied = copy(original)\n\noriginal == copied # -> True\noriginal is copied # -> False\n```\n\n## Installation\n\n```shell\n$ pip install morecopy\n```\n\n## Supported immutable types\n\nThe following types are supported.\nFor mutable types (e.g. `list`) or unsupported immutable types (e.g. `bool`, `NoneType`), `morecopy.copy` and `morecopy.deepcopy` are equivalent to `copy.copy` and `copy.deepcopy`, respectively.\n\nType | `morecopy.copy` | `morecopy.deepcopy`\n--- | --- | ---\n`int` | yes | n/a\n`float` | yes | n/a\n`complex` | yes | n/a\n`str` | yes | n/a\n`bytes` | yes | n/a\n`tuple` | yes | n/a\n`range` | yes | n/a\n`slice` | yes | n/a\n`frozenset` | yes | n/a\n`FunctionType` | yes | n/a\n`LambdaType` | yes | n/a\n\n## Custom immutable copier\n\nUsers can add a custom copy function (copier) for a type.\nFor example, the following code defines copy of integer by creating a copy function and registering it by the `copier_for` decorator.\n\n```python\nfrom morecopy import copier_for\n\n\n@copier_for(int)\ndef copy_int(integer: int) -> int:\n    return eval(repr(integer))\n```\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/astropenguin/morecopy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
