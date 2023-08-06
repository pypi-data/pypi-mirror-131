# units-of-measure
Units of Measure

# Objective

1. Relate [units of measurement](https://en.wikipedia.org/wiki/Unit_of_measurement) to the [International System of Units (SI)](https://www.bipm.org/en/measurement-units/) to define their dimension and magnitude.
2. Relate arbitrary objects to units.

# Motivation

First, I used the library [`forallpeople`](https://github.com/connorferster/forallpeople), but that ran into [issues with large scales](https://github.com/connorferster/forallpeople/issues/27) like megatonnes and gigatonnes.

Based on my [objectives](#objective) I decided to create a new library that does exactly that and does not deal with quantities (yet).

# Get Started

To start from the beginning, open the [Jupyter notebook](https://jupyter-notebook.readthedocs.io/en/latest/) [`start_here.ipynb`](start_here.ipynb).

This library does not require the package `jupyter`, neither at buildtime nor at runtime. Therefore this library does not declare `jupyter` as dependency.

# Develop

1. Test with `pytest`
2. Build with `python3 -m build`
3. Check with `python3 -m twine check dist/*`
4. Publish with `python3 -m twine upload dist/*`
