# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['searcheonet']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'searcheonet',
    'version': '0.1.0',
    'description': 'Python package that allows users to search for information about natural events from the NASA EONET API',
    'long_description': '# searcheonet\n\nPython package that allows users to search for information about natural events from the NASA EONET API\n\n## Installation\n\n```bash\n$ pip install searcheonet\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`searcheonet` was created by Alan Shen. It is licensed under the terms of the Apache License 2.0 license.\n\n## Credits\n\n`searcheonet` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Alan Shen',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
