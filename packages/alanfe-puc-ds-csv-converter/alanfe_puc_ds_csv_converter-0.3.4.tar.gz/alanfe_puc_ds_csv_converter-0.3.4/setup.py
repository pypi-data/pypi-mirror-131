# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alanfe_puc_ds_csv_converter', 'alanfe_puc_ds_csv_converter.model']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'alanfe_puc_ds_csv_converter.converter:converter']}

setup_kwargs = {
    'name': 'alanfe-puc-ds-csv-converter',
    'version': '0.3.4',
    'description': 'A simple module to make easy conversions between two type of files: `csv` and `json`.',
    'long_description': 'IConverter\n===\n\nA simple module to make easy conversions between two type of files: `csv` and `json`.\n<br>\nIt was created for a postgraduate assignment that had as objective to validate our knowledge about the use of basic structures of Python and the process of creating and publishing a Python module.\n\n\n## Usage and Examples\nTo use this module you need to install that end use the convert script of this module:\n```\npip install alanfe-puc-ds-csv-converter\npython3 -m alanfe-puc-ds-csv-converter convert\n```\nYou will set some arguments of this script like: **output path** (using -o or -ouput) and **input path**(using -i or -input). After that automatically it will parse all files in this path and will save it in output path. \n```\npython3 -m alanfe-puc-ds-csv-converter convert -i /input/ -o /output/\n# OR\npython3 -m alanfe-puc-ds-csv-converter convert -i /input/teste.csv -o /output/\n```\nIt will detect if files are csv or json and will convert them to another format, in the case o csv, will be converted to json and json, csv.\n<br>\n<br>\nTo more information about this function we cant use the help command:\n```\npython3 -m alanfe-puc-ds-csv-converter convert --help\n```\n\n\n',
    'author': 'Alan Federich',
    'author_email': 'alan.federich@icloud.com',
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
