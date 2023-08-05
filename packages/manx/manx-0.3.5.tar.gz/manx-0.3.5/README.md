# Manx: Migrations for elasticsearch
[![coverage report](https://gitlab.com/text-analytics/open-source/manx/badges/master/coverage.svg)](https://gitlab.com/text-analytics/open-source/manx/-/commits/master)

[![ML216800971 Manx Shearwater © Kirk Zufelt](https://cdn.download.ams.birds.cornell.edu/api/v1/asset/216800971/1200)](https://macaulaylibrary.org/asset/216800971 "ML216800971 Manx Shearwater © Kirk Zufelt")

Manx is a migration utility for elasticsearch.  It's like [Flyway](https://flywaydb.org/) or [Alembic](https://alembic.sqlalchemy.org/en/latest/), but for elasticsearch.  

> The migration also appears to be quite complex, containing many stopovers and foraging zones
>
> -- <cite>[Manx shearwater - Wikipedia](https://en.wikipedia.org/wiki/Manx_shearwater "Manx shearwater - Wikipedia")</cite>

## Features
* Pure Python implementation
* Automatic index migration and aliaising
* Dynamic migration script execution

Manx officially supports Python 3.8+.

## Installation
To install Manx, simply:

`$ pip install manx`

## Development
Manx uses [poetry](https://python-poetry.org) for dependency management and packaging. To install:

`$ poetry install`

To build the distributable:

`$ poetry build`

To publish the package to [PyPI](https://pypi.org/project/manx/):

`$ poetry publish`

### Standards
Manx uses several tools to ensure code standards:
*  [flake8](https://flake8.pycqa.org/en/latest/): linting
*  [black](https://pypi.org/project/black/): formatting
*  [mypy](https://mypy.readthedocs.io/en/stable/): type hinting
*  [isort](https://timothycrosley.github.io/isort/): import sorting

### Resources
*  [Poetry](https://python-poetry.org)
*  [pytest](https://docs.pytest.org/en/stable/index.html)
*  [pytest-cov](https://github.com/pytest-dev/pytest-cov)
*  [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)
*  [pytest-mock](https://github.com/pytest-dev/pytest-mock/)

## Image Credit
[Manx Shearwater](https://ebird.org/species/manshe "Manx Shearwater") *Puffinus puffinus*  
© Kirk Zufelt  
Juan Fernández, Valparaíso, Chile | 1 Mar 2020  
[Macaulay Library ML216800971](https://macaulaylibrary.org/asset/216800971 "Macaulay Library ML216800971") | [eBird S66021223](https://ebird.org/view/checklist/S66021223 "eBird S66021223") | [The Cornelle Lab](https://www.birds.cornell.edu/home "The Cornelle Lab")