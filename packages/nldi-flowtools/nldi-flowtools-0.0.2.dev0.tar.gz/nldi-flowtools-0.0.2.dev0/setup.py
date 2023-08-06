# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nldi_flowtools', 'nldi_flowtools.process']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.8.0,<2.0.0',
 'click>=7.1.2,<8',
 'geojson>=2.5.0,<3.0.0',
 'numpy>=1.21.0,<2.0.0',
 'pyflwdir==0.5.1',
 'pygeoapi>=0.11.0,<0.12.0',
 'pyproj>=3.3.0,<4.0.0',
 'rasterio>=1.2.9,<2.0.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['nldi-flowtools = nldi_flowtools.__main__:main']}

setup_kwargs = {
    'name': 'nldi-flowtools',
    'version': '0.0.2.dev0',
    'description': 'Nldi Flowtools',
    'long_description': "# Nldi Flowtools\n\n[![PyPI](https://img.shields.io/pypi/v/nldi-flowtools.svg)](https://pypi.org/project/nldi-flowtools/)\n[![Status](https://img.shields.io/pypi/status/nldi-flowtools.svg)](https://pypi.org/project/nldi-flowtools/)\n[![Python Version](https://img.shields.io/pypi/pyversions/nldi-flowtools)](https://pypi.org/project/nldi-flowtools)\n[![License](https://img.shields.io/pypi/l/nldi-flowtools)](https://creativecommons.org/publicdomain/zero/1.0/legalcode)\n\n[![Read the documentation at https://nldi-flowtools.readthedocs.io/](https://img.shields.io/readthedocs/nldi-flowtools/latest.svg?label=Read%20the%20Docs)](https://nldi-flowtools.readthedocs.io/)\n\n[![pipeline status](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-flowtools/badges/main/pipeline.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-flowtools/-/commits/main)\n[![coverage report](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-flowtools/badges/main/coverage.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-flowtools/-/commits/main)\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Poetry](https://img.shields.io/badge/poetry-enabled-blue)](https://python-poetry.org/)\n[![Conda](https://img.shields.io/badge/conda-enabled-green)](https://anaconda.org/)\n\n# Features\n\n- TODO\n\n# Requirements\n\n- TODO\n\n# Installation\n\nYou can install _Nldi Flowtools_ via\n[pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/):\n\n```{.sourceCode .console}\n$ pip install nldi-flowtools\n```\n\n# Usage\n\nPlease see the [Command-line Reference](Usage_) for details.\n\n# Contributing\n\nContributions are very welcome.\nTo learn more, see the Contributor Guide\\_.\n\n# License\n\nDistributed under the terms of the [CC0 1.0 Universal license](https://creativecommons.org/publicdomain/zero/1.0/legalcode),\n_Nldi Flowtools_ is free and open source software.\n\n# Issues\n\nIf you encounter any problems,\nplease [file an issue](https://code.usgs.gov/wma/nhgf/toolsteam/nldi-flowtools/-/issues) along with a detailed description.\n\n# Credits\n\nThis project was generated from\n[@hillc-usgs](https://github.com/hillc-usgs)'s [Pygeoapi Plugin\nCookiecutter](https://code.usgs.gov/wma/nhgf/pygeoapi-plugin-cookiecutter)\ntemplate.\n",
    'author': 'Anders Hopkins',
    'author_email': 'ahopkins@usgs.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://code.usgs.gov/wma/nhgf/toolsteam/nldi-flowtools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
