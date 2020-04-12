# COVID-19 visualization tool

Visualization tool to display real-time COVID-19 tests performed in Catalunya. Data is fed from ["Dades obertes COVID-19"](http://governobert.gencat.cat/ca/dades_obertes/dades-obertes-covid-19).

# Development

In order to contribute to this repo and develop locally, you must install the python environment:

```
pipenv install
```

Make sure Python3.7+ and Pipenv are installed.

## Run app

App can be locally deployed by typing (make sure you installed the environment, as detailed above):

```
pipenv shell run app.py
```

# Future work

The next features to be considered, ordered by decreasing priority, are:

1. Allow displaying positive rate per ABS region.
1. Allow displaying test rate according to ABS region population density.
1. Allow displaying positive rate according to region population density.
1. Add pre-commit hook to make sure requirements is aligned with Pipfile.
1. Add flake8/pylint pre-commit hooks.

