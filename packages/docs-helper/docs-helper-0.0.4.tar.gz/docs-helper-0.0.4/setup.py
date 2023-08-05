# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docs_helper']

package_data = \
{'': ['*']}

install_requires = \
['sphobjinv>=2.1,<3.0']

setup_kwargs = {
    'name': 'docs-helper',
    'version': '0.0.4',
    'description': 'Kickstart repo',
    'long_description': '# docs-helper\n\n- [docs-helper](#docs-helper)\n\n[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/viktorfreiman/py-dev-init)\n\nFor setup see [development.rst](docs/development.rst)\n',
    'author': 'Viktor Freiman',
    'author_email': 'freiman.viktor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/viktorfreiman/docs-helper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
