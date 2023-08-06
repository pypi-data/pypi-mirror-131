<p align="left">
    <a href="https://github.com/metastore-developers/metastore" title="Metastore">
        <img src="https://metastore.readthedocs.io/en/latest/_static/logo.svg" width="128px"/>
    </a>
</p>

[![Releases](https://img.shields.io/github/v/release/metastore-developers/metastore?color=blue)](https://github.com/metastore-developers/metastore/releases)
[![Issues](https://img.shields.io/github/issues/metastore-developers/metastore?color=blue)](https://github.com/metastore-developers/metastore/issues)
[![Pull requests](https://img.shields.io/github/issues-pr/metastore-developers/metastore?color=blue)](https://github.com/metastore-developers/metastore/pulls)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://metastore.readthedocs.io)
[![License](https://img.shields.io/pypi/l/metastore?color=blue)](https://metastore.readthedocs.io/en/latest/license.html)

# Metastore

Metastore Python SDK.

Feature store and data catalog for machine learning.

## Prerequisites

* [Python (>=3.7.0)](https://www.python.org)

## Installation

### Production

Install package:

```
pip install metastore
```

### Development

Install package:

```
pip install -e .[development]
```

> **Note** Use the `-e, --editable` flag to install the package in development mode.

Format source code:

```
autopep8 --recursive --in-place setup.py metastore/ tests/
```

Lint source code:

```
pylint setup.py metastore/ tests/
```

Test package:

```
pytest
```

Report test coverage:

```
pytest --cov --cov-fail-under 80
```

> **Note** Set the `--cov-fail-under` flag to 80% to validate the code coverage metric.

Generate documentation:

```
sphinx-apidoc -f -e -T -d 2 -o docs/metastore/api-reference/ metastore/
```

Build documentation (optional):

```
cd docs/
sphinx-build -b html metastore/ build/
```

## Documentation

Please refer to the official [Metastore Documentation](https://metastore.readthedocs.io) for more information.

## Changelog

[Changelog](https://metastore.readthedocs.io/en/latest/changelog.html) contains information about new features, improvements, known issues, and bug fixes in each release.

## Copyright and license

Copyright (c) 2022, Metastore Developers. All rights reserved.

Project developed under a [BSD-3-Clause License](https://metastore.readthedocs.io/en/latest/license.html).
