# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['todopyedu']

package_data = \
{'': ['*'], 'todopyedu': ['dist/*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'prettytable>=2.4.0,<3.0.0',
 'shellingham>=1.4.0,<2.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['todopyeduP = todopyedu.__main__:main']}

setup_kwargs = {
    'name': 'todopyedup',
    'version': '0.1.0',
    'description': 'Issue log created by educational purposes',
    'long_description': '# python-todo\n\n',
    'author': 'kekbek',
    'author_email': 'vadyusha.surin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/kekbek/python-todo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
