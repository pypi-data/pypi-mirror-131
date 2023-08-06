# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text_alignment_tool',
 'text_alignment_tool.alignment_algorithms',
 'text_alignment_tool.alignment_tool',
 'text_alignment_tool.analyzers',
 'text_alignment_tool.find_wordlist_for_alignment',
 'text_alignment_tool.shared_classes',
 'text_alignment_tool.text_loaders',
 'text_alignment_tool.text_transformers']

package_data = \
{'': ['*']}

install_requires = \
['bidict>=0.21.4,<0.22.0',
 'cursive-re>=0.0.4,<0.0.5',
 'dotmap>=1.3.26,<2.0.0',
 'edlib>=1.3.9,<2.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'lxml>=4.7.1,<5.0.0',
 'minineedle>=3.0.0,<4.0.0',
 'numpy>=1.21.4,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'python-Levenshtein>=0.12.2,<0.13.0',
 'swalign>=0.3.6,<0.4.0',
 'terminaltables>=3.1.10,<4.0.0']

setup_kwargs = {
    'name': 'text-alignment-tool',
    'version': '0.2.14',
    'description': 'A tool for performing complex text alignment processes.',
    'long_description': None,
    'author': 'Bronson Brown-deVost',
    'author_email': 'bronsonbdevost@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
