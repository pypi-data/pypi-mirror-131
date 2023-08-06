# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['patric_converte']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.12b0,<22.0',
 'click>=8.0.3,<9.0.0',
 'flake8>=4.0.1,<5.0.0',
 'ipython>=7.30.1,<8.0.0',
 'isort>=5.10.1,<6.0.0',
 'mypy>=0.910,<0.911']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'patric_converte.converter:conversor_de_csv_para_json',
                     'json_converter = '
                     'patric_converte.converter:conversor_de_json_para_csv']}

setup_kwargs = {
    'name': 'patric-converte',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'Patric Rocha',
    'author_email': 'patric_rocha@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
