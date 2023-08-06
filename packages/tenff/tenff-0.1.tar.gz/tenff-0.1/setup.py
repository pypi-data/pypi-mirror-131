# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tenff']

package_data = \
{'': ['*'], 'tenff': ['data/*']}

entry_points = \
{'console_scripts': ['10ff = tenff.__main__:main']}

setup_kwargs = {
    'name': 'tenff',
    'version': '0.1',
    'description': 'A certain typing contest site spin-off in CLI',
    'long_description': '10ff\n----\n\nA certain typing contest site spin-off in CLI, without all the advertisements,\ntracking and 10 megabytes of AJAX crap.\n\n#### Example\n\n![](https://raw.githubusercontent.com/rr-/10ff/blob/example.gif)\n\n#### Installation\n\n```\ngit clone https://github.com/rr-/10ff\ncd 10ff\npip install --user .\n10ff\n```\n\n#### Running without installation\n\n```\ngit clone https://github.com/rr-/10ff\ncd 10ff\npython3 -m tenff\n```\n',
    'author': 'Marcin Kurczewski',
    'author_email': 'rr-@sakuya.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rr-/10ff',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
