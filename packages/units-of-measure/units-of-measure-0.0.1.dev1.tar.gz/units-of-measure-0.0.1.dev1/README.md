# Units of Measure

as defined in [Unit of Measurement](https://en.wikipedia.org/wiki/Unit_of_measurement).

- Python library: [`units-of-measure`](https://pypi.org/project/units-of-measure/)
- Python package: [`unitsofmeasure`](https://github.com/gerald-scharitzer/units-of-measure/tree/main/unitsofmeasure)

# Objective

1. Relate [units of measurement](https://en.wikipedia.org/wiki/Unit_of_measurement) to the [International System of Units (SI)](https://www.bipm.org/en/measurement-units/) to define their dimension and magnitude.
2. Relate arbitrary objects to units.

# Motivation

First, I used the library [`forallpeople`](https://github.com/connorferster/forallpeople), but that ran into [issues with large scales](https://github.com/connorferster/forallpeople/issues/27) like megatonnes and gigatonnes.

Based on my [objectives](#objective) I decided to create a new library that does exactly that and does not deal with quantities (yet).

# Get Started

To start from the beginning, open the [Jupyter notebook](https://jupyter-notebook.readthedocs.io/en/latest/) [`start_here.ipynb`](start_here.ipynb).

This library does not require the package `jupyter`, neither at buildtime nor at runtime. Therefore this library does not declare `jupyter` as dependency.

Download and install the library with `python -m pip install units-of-measure`.

# Develop

1. Clone with `git clone https://github.com/gerald-scharitzer/units-of-measure.git`
2. Test with `pytest`
3. Build with `python -m build`
4. Check with `python -m twine check dist/*`
5. Publish with `python -m twine upload dist/*`
