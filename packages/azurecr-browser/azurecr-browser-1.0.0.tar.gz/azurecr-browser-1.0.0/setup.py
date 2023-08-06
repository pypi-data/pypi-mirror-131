# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['azurecr_browser', 'azurecr_browser.renderables', 'azurecr_browser.widgets']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'azure-containerregistry>=1.0.0b7,<2.0.0',
 'azure-identity>=1.7.1,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'fast-autocomplete[pylev]>=0.9.0,<0.10.0',
 'importlib-metadata>=4.10.0,<5.0.0',
 'pyperclip>=1.8.2,<2.0.0',
 'rich>=10.11.0,<11.0.0',
 'textual-inputs>=0.2.0,<0.3.0',
 'textual>=0.1.12,<0.2.0',
 'toml>=0.10.2,<0.11.0',
 'validators>=0.18.2,<0.19.0']

entry_points = \
{'console_scripts': ['acr = azurecr_browser.app:run']}

setup_kwargs = {
    'name': 'azurecr-browser',
    'version': '1.0.0',
    'description': 'A terminal user interface for managing artifacts in Azure Container Registry',
    'long_description': None,
    'author': 'Sam Dobson',
    'author_email': '1309834+samdobson@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
