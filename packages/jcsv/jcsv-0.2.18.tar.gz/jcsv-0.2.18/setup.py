# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jcsv']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'pathlib>=1.0.1,<2.0.0']

entry_points = \
{'console_scripts': ['csv2json = jcsv.converter:csvJson',
                     'json2csv = jcsv.converter:jsonCsv']}

setup_kwargs = {
    'name': 'jcsv',
    'version': '0.2.18',
    'description': 'Convert csv to json and convert json to csv ',
    'long_description': '# JCSV (JSON2CSV and CSV2JSON converter)\n\nProject developed in the Python for Data Science course - Artificial intelligence PUC-MG\n\n## Requirements\n- python ^3.7\n\n## Install\n```\npip install jcsv\nor\npip3 install jcsv\n```\n\n## Usage\n\n\n\n- convert csv to json\n\n```\ncsv2json --input /path/to/csv/files --output /path/to/json/files --delimiter ,\n```\n\n- convert json to csv\n\n```\njson2csv --input /path/to/json/files --output /path/to/csv/files --delimiter ,\n```\n\n### Default\n- input = "./"\n- output = "./"\n- delimiter = ","\n\n## Help\n\n```\ncsv2json --help\nUsage: csv2json [OPTIONS]\n\nOptions:\n  -i, --input TEXT      Path where to find CSV files to be contered to JSON.\n  -o, --output TEXT     Path where the converted files will be saved.\n  -d, --delimiter TEXT  Separator used to split files.\n  --help                Show this message and exit.\n```\n\n```\njson2csv --help\nUsage: json2csv [OPTIONS]\n\nOptions:\n  -i, --input TEXT      Path where to find JSON files to be contered to CSV.\n  -o, --output TEXT     Path where the converted files will be saved.\n  -d, --delimiter TEXT  Separator used to split files.\n  --help                Show this message and exit.\n```\n\n',
    'author': 'Deangellis Césari de Oliveira Santiago',
    'author_email': 'deangellis1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
