# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alanfe_puc_ds_csv_converter', 'alanfe_puc_ds_csv_converter.model']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['converter = '
                     'alanfe_puc_ds_csv_converter.converter:converter']}

setup_kwargs = {
    'name': 'alanfe-puc-ds-csv-converter',
    'version': '0.3.6',
    'description': 'A simple module to make easy conversions between two type of files: `csv` and `json`.',
    'long_description': "It is a simple module to make easy conversions between two type of files: **csv** and **json**.\n<br>\nIt has been created for a postgraduate assignment that had as objective to validate our knowledge about the use of basic structures of Python and the process of creating and publishing a Python module.\n\n\n## Usage and Examples\nTo use this module is necessary to install it and use the convert script of this module:\n```\npip install alanfe-puc-ds-csv-converter\npython3 -m alanfe-puc-ds-csv-converter convert\n```\nYou will need to set some arguments of this script like **output path** (using -o or --ouput) and **input path**(using -i or --input). After that automatically it will parse all files in this path and will save them in the output path.  \n```\npython3 -m alanfe-puc-ds-csv-converter convert -i /input/ -o /output/\n# OR\npython3 -m alanfe-puc-ds-csv-converter convert -i /input/teste.csv -o /output/\n```\nIt will detect if the files are csv files or json files and will convert them to another format. In the case of csv files, they will be converted to json. In the case of json files, they will be converted to csv.\n<br>\nA good property of this module is the parallel processing. You can set **--parallel** or **-p** as true and the library's processing will happen in parallel\n```\npython3 -m alanfe-puc-ds-csv-converter convert -i /input/teste.csv -o /output/ --parallel true\n```\n<br>\nTo more information about this module execution we cant use the help command:\n\n```\npython3 -m alanfe-puc-ds-csv-converter convert --help\n```\n\n\n",
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
