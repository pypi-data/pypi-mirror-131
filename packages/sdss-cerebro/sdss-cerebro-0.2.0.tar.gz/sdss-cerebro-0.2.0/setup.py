# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cerebro', 'cerebro.sources']

package_data = \
{'': ['*'], 'cerebro': ['etc/*']}

install_requires = \
['click-default-group>=1.2.2,<2.0.0',
 'click>=8.0.0,<9.0.0',
 'daemonocle>=1.0.2,<2.0.0',
 'influxdb-client>=1.9.0,<2.0.0',
 'ntplib>=0.3.4,<0.4.0',
 'numpy>=1.17.4,<2.0.0',
 'sdss-clu>=1.5.5,<2.0.0',
 'sdss-drift>=0.4.0,<0.5.0',
 'sdsstools>=0.4.0']

entry_points = \
{'console_scripts': ['cerebro = cerebro.__main__:main']}

setup_kwargs = {
    'name': 'sdss-cerebro',
    'version': '0.2.0',
    'description': 'Telemetry management and time series for SDSS-V',
    'long_description': "# cerebro\n\n![Versions](https://img.shields.io/badge/python->3.7-blue)\n[![Documentation Status](https://readthedocs.org/projects/sdss-cerebro/badge/?version=latest)](https://sdss-cerebro.readthedocs.io/en/latest/?badge=latest)\n[![Test Status](https://github.com/albireox/cerebro/workflows/Test/badge.svg)](https://github.com/sdss/sdss/actions)\n[![codecov](https://codecov.io/gh/sdss/cerebro/branch/main/graph/badge.svg)](https://codecov.io/gh/sdss/cerebro)\n\nA library to gather time-series data from different sources and store them, with focus on InfluxDB databases. Documentation and concepts are defined [here](https://sdss-cerebro.readthedocs.io/).\n\n## Installation\n\nIn general you should be able to install `cerebro` by doing\n\n```console\npip install sdss-cerebro\n```\n\nTo build from source, use\n\n```console\ngit clone git@github.com:sdss/cerebro\ncd cerebro\npip install .\n```\n\n## Use\n\n`cerebro` is meant to run as a daemon. The simplest way to run it is simply\n\n```console\ncerebro start\n```\n\nThis will run all the sources and use all the observers. You can define a specific profile to use\n\n```console\ncerebro --profile lvm-lab start\n```\n\nor a series of sources\n\n```console\ncerebro --sources lvm_govee_clean_room,lvm_sens4_r1 start\n```\n\nNormally `cerebro` will run in detached/daemon mode. It's also possible to pass the flag `--debug` (`cerebro start --debug`) to run the code in the foreground.\n\nRun `cerebro --help` to get all the options available.\n\n## Development\n\n`cerebro` uses [poetry](http://poetry.eustace.io/) for dependency management and packaging. To work with an editable install it's recommended that you setup `poetry` and install `cerebro` in a virtual environment by doing\n\n```console\npoetry install\n```\n\nPip does not support editable installs with PEP-517 yet. That means that running `pip install -e .` will fail because `poetry` doesn't use a `setup.py` file. As a workaround, you can use the `create_setup.py` file to generate a temporary `setup.py` file. To install `cerebro` in editable mode without `poetry`, do\n\n```console\npip install poetry\npython create_setup.py\npip install -e .\n```\n\nThe style code is [black](https://black.readthedocs.io/en/stable/).\n",
    'author': 'José Sánchez-Gallego',
    'author_email': 'gallegoj@uw.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sdss/cerebro',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
