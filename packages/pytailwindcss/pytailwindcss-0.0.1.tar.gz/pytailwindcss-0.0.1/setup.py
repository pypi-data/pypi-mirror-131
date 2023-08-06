# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytailwindcss']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['tailwindcss = pytailwindcss.__main__:main']}

setup_kwargs = {
    'name': 'pytailwindcss',
    'version': '0.0.1',
    'description': 'Install and invoke tailwindcss from Python',
    'long_description': '# Tailwind CSS binary Python bindings\n\n[WIP]\n\nRun *TailwindCSS* binary in *Python* without *Node*!\n',
    'author': 'Tim Kamanin',
    'author_email': 'tim@timonweb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/timonweb/pytailwindcss',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
