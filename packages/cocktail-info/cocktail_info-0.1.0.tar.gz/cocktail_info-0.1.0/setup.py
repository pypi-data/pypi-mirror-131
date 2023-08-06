# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cocktail_info']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=7.30.1,<8.0.0', 'pandas>=1.3.5,<2.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'cocktail-info',
    'version': '0.1.0',
    'description': 'Get the information of cocktails.',
    'long_description': '# cocktail_info\n\nGet the information of cocktails.\n\n## Installation\n\n```bash\n$ pip install cocktail_info\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`cocktail_info` was created by Kun Yao. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`cocktail_info` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Kun Yao',
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
