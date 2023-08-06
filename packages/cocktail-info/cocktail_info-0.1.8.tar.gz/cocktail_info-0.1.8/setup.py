# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cocktail_info']

package_data = \
{'': ['*']}

install_requires = \
['ipython==7.29.0', 'pandas==1.3.4', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'cocktail-info',
    'version': '0.1.8',
    'description': 'Get the information of cocktails.',
    'long_description': "# cocktail_info\n\nThis project is called cocktail_info. The functions are built to get the information of cocktails users want to know. Below are the explanations for what each function can do:\n\nFunction get_id(): This function can help users to get the id of the cocktail they input so that they could use for further search.\n\nFunction get_cocktail(): This function can help users to get the details of the cocktails they input, such as ID, Name, Category, whether they contain alcohol, the ways to make them, etc.\n\nFunction get_one(): This function can help users to get the information of the exact one cocktail they want through the unique id.\n\nFunction get_ingredient(): This function can help users to get the names and measures of the ingredients in the cocktail after the users input the name of cocktails. \n\nFunction get_pics(): This function can help users to get the pictures of the cocktails along with the IDs and names they input.\n\nFunction decsription(): This function can give users the introduction of cocktails users input.\n\nFunction is_in(): This function allows users to check whether the ingredient they input is in the ingredients list.\n\n## Installation\n\n```bash\n$ pip install cocktail_info\n```\n\n## Usage\n\n```bash\nfrom cocktail_info import cocktail_info\n```\n\n### Get the id of the cocktail\n\n```bash\ncocktail_info.get_id('gin')\n```\n\n### Get the information of the cocktails\n\n```bash\ncocktail_info.get_cocktail('gin')\n```\n\n### Get the information of the exact cocktail you want to know\n\n```bash\ncocktail_info.get_one('gin')\n```\n\n### Get the ingredients of the cocktails\n\n```bash\ncocktail_info.get_ingredient('gin')\n```\n\n### Get the pictures of the cocktails\n\n```bash\ncocktail_info.get_pics('gin')\n```\n\n### Get the introduction of the cocktail\n\n```bash\ncocktail_info.description('gin')\n```\n\n### Tell whether one ingredient is in the cocktail\n\n```bash\ncocktail_info.is_in('gin')\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`cocktail_info` was created by Kun Yao. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`cocktail_info` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n",
    'author': 'Kun Yao',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kenyaokun/cocktail_info',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
