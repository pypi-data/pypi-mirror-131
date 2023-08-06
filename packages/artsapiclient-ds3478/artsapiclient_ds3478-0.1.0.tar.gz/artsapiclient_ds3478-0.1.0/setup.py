# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['artsapiclient_ds3478']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.5,<2.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'artsapiclient-ds3478',
    'version': '0.1.0',
    'description': "API Client for the Art Institute of Chicago's API which provides JSON formatted data as a REST style service that allows developers to explore and integrate the museum's public data into their projects.",
    'long_description': "# artsapiclient_ds3478\n\nAPI Client for the Art Institute of Chicago's API which provides JSON formatted data as a REST style service that allows developers to explore and integrate the museum's public data into their projects.\n\n## Installation\n\n```bash\n$ pip install artsapiclient_ds3478\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`artsapiclient_ds3478` was created by Donald Stephens. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`artsapiclient_ds3478` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n",
    'author': 'Donald Stephens',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
