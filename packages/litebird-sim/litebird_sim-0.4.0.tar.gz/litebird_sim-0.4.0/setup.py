# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['litebird_sim',
 'litebird_sim.destriper',
 'litebird_sim.hwp_sys',
 'litebird_sim.imo',
 'litebird_sim.mbs']

package_data = \
{'': ['*'],
 'litebird_sim': ['datautils/*'],
 'litebird_sim.hwp_sys': ['examples/*'],
 'litebird_sim.mbs': ['fg_models/*']}

install_requires = \
['PyGithub>=1.53,<2.0',
 'asciimatics>=1.12.0,<2.0.0',
 'astropy>=4.0,<5.0',
 'backports-datetime-fromisoformat>=1.0.0,<2.0.0',
 'black>=21.9b,<22.0',
 'ducc0>=0.20.0,<0.21.0',
 'flake8>=3.7,<4.0',
 'h5py==3.4',
 'healpy>=1.15.0,<2.0.0',
 'jinja2>=3.0,<4.0',
 'jplephem>=2.14,<3.0',
 'katex>=0.0.4,<0.0.5',
 'markdown-katex>=202006.1021,<202007.0',
 'markdown>=3.2,<4.0',
 'matplotlib>=3.1,<4.0',
 'numba>=0.54,<0.55',
 'numpy>=1.18,<2.0',
 'pre-commit>=2.15.0,<3.0.0',
 'pybind11>=2.5.0,<3.0.0',
 'pyperclip>=1.8.1,<2.0.0',
 'pysm3>=3.3.0,<4.0.0',
 'pytest>=5.3,<6.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.24.0,<3.0.0',
 'rich>=6.2.0,<7.0.0',
 'sphinx>=4.2,<5.0',
 'sphinx_rtd_theme>=0.4.3,<0.5.0',
 'sphinxcontrib-bibtex>=2.4.0,<3.0.0',
 'sphinxcontrib-contentui>=0.2.5,<0.3.0',
 'sphinxcontrib.asciinema>=0.2.1,<0.3.0',
 'toast-cmb>=2.3.14,<3.0.0',
 'tomlkit>=0.5.8,<0.6.0']

extras_require = \
{'jupyter': ['jupyter>=1.0,<2.0'], 'mpi': ['mpi4py>=3.0,<4.0']}

setup_kwargs = {
    'name': 'litebird-sim',
    'version': '0.4.0',
    'description': 'Simulation tools for the LiteBIRD experiment',
    'long_description': '<!--\nTemplate taken from https://github.com/othneildrew/Best-README-Template\n\n*** To avoid retyping too much info. Do a search and replace for the following:\n*** github_username, repo, twitter_handle, email\n-->\n\n\n<!-- PROJECT SHIELDS -->\n<!--\n*** I\'m using markdown "reference style" links for readability.\n*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).\n*** See the bottom of this document for the declaration of the reference variables\n*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.\n*** https://www.markdownguide.org/basic-syntax/#reference-style-links\n-->\n[![Stable](https://img.shields.io/badge/docs-stable-blue.svg)](https://litebird-sim.readthedocs.io/en/master/)\n[![Tests](https://github.com/litebird/litebird_sim/workflows/Tests/badge.svg?branch=master&event=push)](https://github.com/litebird/litebird_sim/actions?query=workflow%3ATests+branch%3Amaster)\n[![Build Status](https://ci.appveyor.com/api/projects/status/github/litebird/litebird-sim?svg=true)](https://ci.appveyor.com/project/litebird/litebird-sim)\n[![Issues][issues-shield]][issues-url]\n[![GPL3 License][license-shield]][license-url]\n\n\n<!-- PROJECT LOGO -->\n<br />\n<p align="center">\n  <a href="https://github.com/litebird/litebird_sim">\n    <img src="images/logo.png" alt="Logo" width="80" height="80">\n  </a>\n\n  <h3 align="center">LiteBIRD Simulation Framework</h3>\n\n  <p align="center">\n    Main repository of the LiteBIRD Simulation Framework, a set of Python modules to simulate the instruments onboard the LiteBIRD spacecraft.\n    <br />\n    <a href="https://litebird-sim.readthedocs.io/en/master/"><strong>Explore the docs »</strong></a>\n    <br />\n    <br />\n    <a href="https://litebird-sim.readthedocs.io/en/master/tutorial.html">View Demo</a>\n    ·\n    <a href="https://github.com/litebird/litebird_sim/issues">Report Bug</a>\n    ·\n    <a href="https://github.com/litebird/litebird_sim/issues">Request Feature</a>\n  </p>\n</p>\n\n\n\n<!-- TABLE OF CONTENTS -->\n## Table of Contents\n\n* [About the Project](#about-the-project)\n  * [Built With](#built-with)\n* [Getting Started](#getting-started)\n  * [Prerequisites](#prerequisites)\n  * [Installation](#installation)\n* [Usage](#usage)\n* [Roadmap](#roadmap)\n* [Contributing](#contributing)\n* [License](#license)\n* [Contact](#contact)\n* [Acknowledgements](#acknowledgements)\n\n\n\n<!-- ABOUT THE PROJECT -->\n## About The Project\n\nThe LiteBIRD Simulation Framework is being developed for the\n[LiteBIRD collaboration](http://litebird.jp/eng/).\n\n\n### Built With\n\n-   Love!\n-   [Python 3](https://www.python.org)\n-   [Poetry](https://python-poetry.org/)\n-   [NumPy](https://numpy.org)\n-   [Astropy](https://www.astropy.org)\n-   [Healpix](https://healpix.jpl.nasa.gov)\n-   [Sphinx](https://www.sphinx-doc.org/en/master/)\n-   [Numba](https://numba.pydata.org/)\n-   [ducc](https://github.com/litebird/ducc)\n\n\n<!-- GETTING STARTED -->\n## Getting Started\n\nRefer to the\n[documentation](https://litebird-sim.readthedocs.io/en/master/installation.html)\nto learn how to install the LiteBIRD simulation framework on your\ncomputer or on a HPC cluster.\n\n\n<!-- USAGE EXAMPLES -->\n## Usage\n\nThe documentation is available online at\n[litebird-sim.readthedocs.io/en/master/](https://litebird-sim.readthedocs.io/en/master/).\n\nTo create a local copy of the documentation, make sure you ran\n`poetry` with the flag `--extras=docs`, then run the following\ncommand:\n\n-   Linux or Mac OS X:\n    ```\n    ./refresh_docs.sh\n    ```\n\n-   Windows:\n    ```\n    poetry shell\n    cd docs\n    make.bat html\n    ```\n\n\n<!-- ROADMAP -->\n## Roadmap\n\nSee the [open issues](https://github.com/litebird/litebird_sim/issues)\nfor a list of proposed features (and known issues).\n\n\n<!-- CONTRIBUTING -->\n## Contributing\n\nIf you are part of the LiteBIRD collaboration and have something that\nmight fit in this framework, you\'re encouraged to contact us! Any\ncontributions you make are **greatly appreciated**.\n\n1.  Read [CONTRIBUTING.md](https://github.com/litebird/litebird_sim/blob/master/CONTRIBUTING.md)\n2.  Fork the project\n3.  Create your feature branch (`git checkout -b feature/AmazingFeature`)\n4.  Commit your changes (`git commit -m \'Add some AmazingFeature\'`)\n5.  Push to the Branch (`git push origin feature/AmazingFeature`)\n6.  Open a Pull Request\n\n\n<!-- LICENSE -->\n## License\n\nDistributed under the [GPL3 License][license-url].\n\n\n<!-- CONTACT -->\n## Contact\n\nLiteBIRD Simulation Team - litebird_pipe@db.ipmu.jp\n\nProject Link: [https://github.com/litebird/litebird_sim](https://github.com/litebird/litebird_sim)\n\n\n\n<!-- ACKNOWLEDGEMENTS -->\n## How to cite this code\n\nTODO!\n\n\n<!-- MARKDOWN LINKS & IMAGES -->\n<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->\n[issues-shield]: https://img.shields.io/github/issues/litebird/litebird_sim?style=flat-square\n[issues-url]: https://github.com/litebird/litebird_sim/issues\n[license-shield]: https://img.shields.io/github/license/litebird/litebird_sim.svg?style=flat-square\n[license-url]: https://github.com/litebird/litebird_sim/blob/master/LICENSE\n\n<!-- Once we have some nice screenshot, let\'s put a link to it here! -->\n[product-screenshot]: images/screenshot.png\n',
    'author': 'The LiteBIRD Simulation Team',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
