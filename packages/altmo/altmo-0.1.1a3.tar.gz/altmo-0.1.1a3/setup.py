# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['altmo', 'altmo.api', 'altmo.commands', 'altmo.data']

package_data = \
{'': ['*']}

install_requires = \
['GDAL>=3.2.1,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'click>=8.0.1,<9.0.0',
 'numpy>=1.21.0,<2.0.0',
 'psycopg2>=2.8.6,<3.0.0',
 'rasterio>=1.2.6,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'tqdm>=4.61.0,<5.0.0']

entry_points = \
{'console_scripts': ['altmo = altmo.main:cli']}

setup_kwargs = {
    'name': 'altmo',
    'version': '0.1.1a3',
    'description': 'Tools for mapping walkability and bikeability using Open Street Map data',
    'long_description': '# AltMo\n\n**Alt**ernative **Mo**bilities is a CLI tool which helps map alternative mobilities with Open Street Map data.\nSpecifically, this tool helps you map walkability and bikeability averages as a surface for an area of intent\n(usually a city or a region).\n\nIt relies on the following external services to work:\n\n- A PostgreSQL database within extensions `postgis`, `hstore` and `tablefunc` enabled\n- An Open Street Map database imported into this database\n- A running instance a [Vahalla](https://valhalla.readthedocs.io/en/latest/) (used for calculating network routing)\n- A GeoJSON file of the boundary you would like to gather data for (should fit inside OSM data)\n\nFor a full description of how to use this tool, you are encouraged to visit \n[https://altmo.readthedocs.io/en/latest/index.html](https://altmo.readthedocs.io/en/latest/index.html).\n',
    'author': 'Travis Hathaway',
    'author_email': 'travis.j.hathaway@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://altmo.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
