# Metromobilite
[![PyPI Version](https://img.shields.io/pypi/v/metromobilite.svg)](https://pypi.org/project/metromobilite/)

A Python client for interacting with [Metromobilite API](https://www.metromobilite.fr/pages/opendata/OpenDataApi.html) (Transport for Grenoble, TAG).

Installation
=====

```sh
pip install metromobilite
```


```sh
git clone git@github.com:PierreBerger/metromobilite.git
cd metromobilite
python setup.py install
```

Usage
=====
### Import and initialization:
```python
from metromobilite import Metromobilite
m = Metromobilite(origin='My Origin')
print (m.get_stoptimes('SEM:2216'))
```

All stops and routes are vailable here : [https://data.metromobilite.fr/api/routers/default/index/routes](https://data.metromobilite.fr/api/routers/default/index/routes)

See [Metromobilite API documentation](https://data.metromobilite.fr/donnees) for more informations.