# radiocc

[![license badge]][license file]
[![version badge]][pypi url]
[![python badge]][python url]
[![coverage badge]][coverage url]
[![pre-commit badge]][pre-commit url]

> Radio occulation

---

[Installation](#installation) |
[Usage](#usage) |
[Configuration](#configuration) |
[Roadmap](#roadmap) |
[License](#license)

---

## Installation

```sh
pipx install radiocc
```

installs **radiocc** via [`pipx`][pipx url] to benefit of an isolated environment.

## Usage

If you use **radiocc** as a command-line, you should read the
[command line guide][command-line-guide file].

If you decide to use it from Python, you should read the
[library guide][library-guide file].

## Configuration

**radiocc**
+ runs a list of input folders gathered in a "to_process" folder
+ writes the ouputs and saves figures in a "results" folder

To understand the config file, you should read the
[config file guide][config-file-guide file].

## Roadmap

+ improve old code for lisibility, portability and testing
+ improve CLI interface for parameter tuning
+ improve configuration using the library (most commands exit after their call)
+ provide GUI interface for parameter tuning
+ provide GUI tool on graphs to set thresholds and corrections

## License

Licensed under the [Apache 2.0 license][license file].

[repo url]: https://gitlab-as.oma.be/gregoireh/radiocc
[pypi url]: https://pypi.org/project/radiocc
[pre-commit file]: https://gitlab-as.oma.be/gregoireh/radiocc/-/raw/main/.pre-commit-config.yaml
[command-line-guide file]: https://gitlab-as.oma.be/gregoireh/radiocc/-/blob/main/docs/command-line-guide.md
[library-guide file]: https://gitlab-as.oma.be/gregoireh/radiocc/-/blob/main/docs/library-guide.md
[config-file-guide file]: https://gitlab-as.oma.be/gregoireh/radiocc/-/blob/main/docs/config-file-guide.md
[license file]: https://gitlab-as.oma.be/gregoireh/radiocc/-/raw/main/LICENSE
[license badge]: https://img.shields.io/badge/License-Apache%202.0-blue.svg
[coverage badge]: https://img.shields.io/badge/coverage-0%25-red
[coverage url]: https://github.com/pytest-dev/pytest-cov
[version badge]: https://img.shields.io/badge/version-0.6.9-blue
[python url]: https://www.python.org/
[python badge]: https://img.shields.io/badge/python->=3.9,<3.10-blue
[pre-commit url]: https://pre-commit.com
[pre-commit badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[poetry url]: https://python-poetry.org/docs
[flake8 url]: https://flake8.pycqa.org/en/latest
[isort url]: https://github.com/timothycrosley/isort
[mypy url]: http://mypy-lang.org
[black url]: https://github.com/psf/black
[pytest url]: https://docs.pytest.org/en/latest
[pipx url]: https://github.com/pypa/pipx
