# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['erica_csv_converter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'pandas>=1.3.5,<2.0.0']

entry_points = \
{'console_scripts': ['csv_converter = erica_csv_converter.converter:converter']}

setup_kwargs = {
    'name': 'erica-csv-converter',
    'version': '0.1.4',
    'description': 'Convert CSV to Json',
    'long_description': '# File Converter\n\nCSV to JSON.\nJSON to CSV.\n\n## Introdução\n\n- Trabalho Academico Puc Minas\n\n`` `bash\npipx install erica_csv_converter\n`` `',
    'author': 'Erica Brandão',
    'author_email': 'erica_martins_brandao@yahoo.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
