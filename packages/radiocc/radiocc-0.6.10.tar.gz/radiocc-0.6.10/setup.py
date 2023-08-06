# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['radiocc', 'radiocc.old']

package_data = \
{'': ['*'], 'radiocc': ['assets/information/*', 'assets/interface/*']}

install_requires = \
['PyGObject>=3.42.0,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'arrow>=1.1.1,<2.0.0',
 'bs4>=0.0.1,<0.0.2',
 'cairocffi>=1.3.0,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'colored>=1.4.2,<2.0.0',
 'dotmap>=1.3.24,<2.0.0',
 'envtoml>=0.1.2,<0.2.0',
 'matplotlib>=3.4.3,<4.0.0',
 'nptyping>=1.4.3,<2.0.0',
 'numpy>=1.21.2,<2.0.0',
 'pandas>=1.3.2,<2.0.0',
 'pudb>=2021.1,<2022.0',
 'requests>=2.26.0,<3.0.0',
 'ruamel.yaml>=0.17.16,<0.18.0',
 'scipy>=1.7.1,<2.0.0',
 'spiceypy>=4.0.2,<5.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'urlpath>=1.1.7,<2.0.0']

entry_points = \
{'console_scripts': ['radiocc = radiocc.cli:main']}

setup_kwargs = {
    'name': 'radiocc',
    'version': '0.6.10',
    'description': 'Radio occultations',
    'long_description': '# radiocc\n\n[![license badge]][license file]\n[![version badge]][pypi url]\n[![python badge]][python url]\n[![coverage badge]][coverage url]\n[![pre-commit badge]][pre-commit url]\n\n> Radio occulation\n\n---\n\n[Installation](#installation) |\n[Usage](#usage) |\n[Configuration](#configuration) |\n[Roadmap](#roadmap) |\n[License](#license)\n\n---\n\n## Installation\n\n```sh\npipx install radiocc\n```\n\ninstalls **radiocc** via [`pipx`][pipx url] to benefit of an isolated environment.\n\n## Usage\n\nIf you use **radiocc** as a command-line, you should read the\n[command line guide][command-line-guide file].\n\nIf you decide to use it from Python, you should read the\n[library guide][library-guide file].\n\n## Configuration\n\n**radiocc**\n+ runs a list of input folders gathered in a "to_process" folder\n+ writes the ouputs and saves figures in a "results" folder\n\nTo understand the config file, you should read the\n[config file guide][config-file-guide file].\n\n## Roadmap\n\n+ improve old code for lisibility, portability and testing\n+ improve CLI interface for parameter tuning\n+ improve configuration using the library (most commands exit after their call)\n+ provide GUI interface for parameter tuning\n+ provide GUI tool on graphs to set thresholds and corrections\n\n## License\n\nLicensed under the [Apache 2.0 license][license file].\n\n[repo url]: https://gitlab-as.oma.be/gregoireh/radiocc\n[pypi url]: https://pypi.org/project/radiocc\n[pre-commit file]: https://gitlab-as.oma.be/gregoireh/radiocc/-/raw/main/.pre-commit-config.yaml\n[command-line-guide file]: https://gitlab-as.oma.be/gregoireh/radiocc/-/blob/main/docs/command-line-guide.md\n[library-guide file]: https://gitlab-as.oma.be/gregoireh/radiocc/-/blob/main/docs/library-guide.md\n[config-file-guide file]: https://gitlab-as.oma.be/gregoireh/radiocc/-/blob/main/docs/config-file-guide.md\n[license file]: https://gitlab-as.oma.be/gregoireh/radiocc/-/raw/main/LICENSE\n[license badge]: https://img.shields.io/badge/License-Apache%202.0-blue.svg\n[coverage badge]: https://img.shields.io/badge/coverage-0%25-red\n[coverage url]: https://github.com/pytest-dev/pytest-cov\n[version badge]: https://img.shields.io/badge/version-0.6.10-blue\n[python url]: https://www.python.org/\n[python badge]: https://img.shields.io/badge/python->=3.9,<3.10-blue\n[pre-commit url]: https://pre-commit.com\n[pre-commit badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n[poetry url]: https://python-poetry.org/docs\n[flake8 url]: https://flake8.pycqa.org/en/latest\n[isort url]: https://github.com/timothycrosley/isort\n[mypy url]: http://mypy-lang.org\n[black url]: https://github.com/psf/black\n[pytest url]: https://docs.pytest.org/en/latest\n[pipx url]: https://github.com/pypa/pipx\n',
    'author': 'Ananya Krishnan',
    'author_email': 'ananyakrishnaniiserk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab-as.oma.be/gregoireh/radiocc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
