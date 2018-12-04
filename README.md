# Soundings

Atmospheric sounding reading and plotting utility 

## What
Soundings downloads radiosounding data for a chosen station at a specific date and transforms it in an easy editable form. With the help of [MetPy](https://unidata.github.io/MetPy/latest/) calculations can be executed and plots created (hodograph, skew plot).

## How
It can be used via [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/acinn/soundings/master?filepath=example.ipynb)

If it is used without Binder the following should be installed:
- MetPy [installation](https://unidata.github.io/MetPy/latest/installguide.html) 
- cartopy 
- pandas
- numpy
- matplotlib

## Where
example.ipynb is a jupyter-notebook, in which the application is explained and that can be used for further calculations.

In soundings.py functions are defined, which are tested with the testfunctions in test_soundings.py.


