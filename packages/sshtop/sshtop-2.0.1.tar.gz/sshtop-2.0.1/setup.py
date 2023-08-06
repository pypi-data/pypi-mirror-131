# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sshtop']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0', 'paramiko>=2.8.1,<3.0.0']

entry_points = \
{'console_scripts': ['sshtop = sshtop.__main__:main']}

setup_kwargs = {
    'name': 'sshtop',
    'version': '2.0.1',
    'description': 'Remote server monitoring tool over SSH',
    'long_description': '# sshtop\n\n`sshtop` connects to remote systems over SSH and gathers common information about the system.\n\nOnly Linux systems can be monitored at this moment.\n\n## Installation\n\nInstall using pip:\n```bash\n$ pip install sshtop\n```\n\n## Usage\n\n```bash\n$ sshtop [-h] [-p PORT] [-i IDENTITY_FILE] destination\n```\n\nIf a keyfile has not been supplied, `sshtop` will automatically search for a valid key through a SSH agent.\n\n## License\n\nCopyright (c) 2019-2021 by ***Kamil Marut***.\n\n`sshtop` is under the terms of the [MIT License](https://www.tldrlegal.com/l/mit), following all clarifications stated in the [license file](LICENSE).\n',
    'author': 'Kamil Marut',
    'author_email': 'kamil@kamilmarut.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/exler/sshtop',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
