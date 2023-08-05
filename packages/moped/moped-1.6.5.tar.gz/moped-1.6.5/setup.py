# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moped',
 'moped.core',
 'moped.databases',
 'moped.databases.cyc',
 'moped.databases.cyc.parse',
 'moped.databases.cyc.repair',
 'moped.topological',
 'moped.utils']

package_data = \
{'': ['*']}

install_requires = \
['Meneco==1.5.3',
 'PyYAML>=6.0,<7.0',
 'cobra>=0.22.1,<0.23.0',
 'modelbase==1.2.3',
 'numpy>=1.21.4,<2.0.0',
 'pandas>=1.3.4,<2.0.0',
 'pipdeptree>=2,<3',
 'pyasp>=1.4.4,<2.0.0',
 'python-libsbml>=5.19.0,<6.0.0',
 'tqdm>=4,<5']

setup_kwargs = {
    'name': 'moped',
    'version': '1.6.5',
    'description': 'Stoichiometric metabolic modelling',
    'long_description': '[![pipeline status](https://gitlab.com/marvin.vanaalst/moped/badges/master/pipeline.svg)](https://gitlab.com/marvin.vanaalst/moped/-/commits/master)\n[![coverage report](https://gitlab.com/marvin.vanaalst/moped/badges/master/coverage.svg)](https://gitlab.com/marvin.vanaalst/moped/-/commits/master)\n[![Documentation Status](https://readthedocs.org/projects/moped/badge/?version=latest)](https://moped.readthedocs.io/en/latest/?badge=latest)\n[![PyPi](https://img.shields.io/pypi/v/moped)](https://pypi.org/project/moped/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Downloads](https://pepy.tech/badge/moped)](https://pepy.tech/project/moped)\n\n# moped\n\nA metabolic object-oriented Python modelling environment.\n\n## Installation\n\nPlease consult our [installation tutorial](https://gitlab.com/marvin.vanaalst/moped/-/blob/master/docs/source/installation-guide.md)\n\n## Release notes\n\nmoped is currently in an alpha stage\n\n## Documentation\n\nThe official documentation will be hosted on readthedocs\n\n## Tutorials\n\nCheck out our tutorial on [readthedocs](https://moped.readthedocs.io/en/latest/source/tutorial.html) or [here](https://gitlab.com/marvin.vanaalst/moped/-/blob/master/docs/source/tutorial.ipynb) \n\n## Troubleshooting\n\nIf you encounter any bugs, please first consult our [troubleshooting](https://gitlab.com/marvin.vanaalst/moped/-/blob/master/docs/source/troubleshooting.md)\nguide and if you cannot find an answer feel free to open an issue.\n\n## Contributing\n\nAll contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.\nIf you want to contribute code to the project, please consider our [contribution guide](https://gitlab.com/marvin.vanaalst/moped/-/blob/master/CONTRIBUTING.md)\n\n## License\n\nmoped is licensed under [GPL 3](https://gitlab.com/marvin.vanaalst/moped/-/blob/master/LICENSE)\n\n## Issues and support\n\nIf you experience issues using the software please contact us through our [issues](https://gitlab.com/marvin.vanaalst/moped/issues) page.\n',
    'author': 'Marvin van Aalst',
    'author_email': 'marvin.vanaalst@gmail.com',
    'maintainer': 'Marvin van Aalst',
    'maintainer_email': 'marvin.vanaalst@gmail.com',
    'url': 'https://gitlab.com/marvin.vanaalst/moped',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
