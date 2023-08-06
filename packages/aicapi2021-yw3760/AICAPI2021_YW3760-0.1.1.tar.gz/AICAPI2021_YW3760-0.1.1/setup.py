# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aicapi2021_yw3760']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.5,<2.0.0']

setup_kwargs = {
    'name': 'aicapi2021-yw3760',
    'version': '0.1.1',
    'description': 'This is a python package of an API CLIENT to retrieve the data of collections in the Atr Institute of Chicago. The outputs inlude: An table include related information about the searched artworks. An table include related information about the searched tours. An image of an artwork, searched by title and artist. An table include related information about the searched products.',
    'long_description': '# AICAPI2021_YW3760\n\nThis is a python package of an API CLIENT to retrieve the data of collections in the Atr Institute of Chicago. The outputs inlude: An table include related information about the searched artworks. An table include related information about the searched tours. An image of an artwork, searched by title and artist. An table include related information about the searched products.\n\n## Installation\n\n```bash\n$ pip install AICAPI2021_YW3760\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`AICAPI2021_YW3760` was created by YW3760. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`AICAPI2021_YW3760` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'YW3760',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tbrambor/qmsspkg',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
