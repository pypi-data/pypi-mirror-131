# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['littlesis']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.5,<2.0.0', 'ratelimit>=2.2.1,<3.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'littlesis',
    'version': '0.1.0',
    'description': 'Python wrapper for the LittleSis API.',
    'long_description': '# littlesis\n\nPython wrapper for the LittleSisAPI.\n\n## Installation\n\n```bash\n$ pip install littlesis\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`littlesis` was created by Brendan Mapes. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`littlesis` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Brendan Mapes',
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
