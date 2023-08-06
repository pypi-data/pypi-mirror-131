# Obelist

_A CLI tool for generating standard annotations for linting tools, tests, and so on (including support for GitHub Actions)_

[![Build][action-build-img]][action-build]

**Table of contents:**

- [Installation](#installation)
- [Usage](#usage)
- [Appendix](#appendix)
  - [Etymology](#etymology)

## Installation

The [obelist][pypi-obelist] package is published to [PyPI][pypi].

Because Obelist is primarily designed to be used as a CLI tool, we recommend that you install the package in an isolated virtual environment using [pipx][pipx], like so:

```console
$ pipx install obelist
```

However, if you want to install Obelist as a library, you can also install the package using [pip][pip]:

```console
$ pip install obelist
```

## Usage

For basic usage information, run:

```console
$ obelist
```

For more detailed help, run:

```console
$ obelist --help
```

## Appendix

### Etymology

The [obelus] is a typographical mark used to "indicate erroneous or dubious content." The _Oxford English Dictionary_ (OED) defines [obelism] as the "action or practice of marking something as spurious."

Obelist, then, serves as both a verbal noun and a play on words: the program's output is, essentially, _a list of obeluses_.

[action-build-img]: https://github.com/nomiro/obelist/actions/workflows/build.yaml/badge.svg
[action-build]: https://github.com/nomiro/obelist/actions/workflows/build.yaml
[obelism]: https://en.wikipedia.org/wiki/Obelism
[obelus]: https://en.wikipedia.org/wiki/Obelus
[pip]: https://pip.pypa.io/en/stable/
[pipx]: https://pypa.github.io/pipx/
[pypi-obelist]: https://pypi.org/project/obelist
[pypi]: https://pypi.org/
