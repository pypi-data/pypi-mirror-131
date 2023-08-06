# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aicapi_yw3760']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0', 'ipython>=7.30.1,<8.0.0', 'pandas>=1.3.5,<2.0.0']

setup_kwargs = {
    'name': 'aicapi-yw3760',
    'version': '0.1.2',
    'description': 'This is a python package of an API CLIENT to retrieve the data of collections in the Atr Institute of Chicago.',
    'long_description': '# aicapi_yw3760\n\nThis is a python package of an API CLIENT to retrieve the data of collections in the Atr Institute of Chicago.\nThe outputs inlude:\nAn table include related information about the searched artworks.\nAn table include related information about the searched tours.\nAn image of an artwork, searched by title and artist.\nAn table include related information about the searched products.\n\n## Installation\n\n```bash\n$ pip install aicapi_yw3760\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`aicapi_yw3760` was created by yw3760. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`aicapi_yw3760` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'yw3760',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nicolewang97/AICAPI_YW3760',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
