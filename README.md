# Soundings

Atmospheric sounding reading and plotting utility.

This tool downloads radiosounding data from the
[University of Wyoming portal](http://weather.uwyo.edu/upperair/sounding.html)
for a chosen station at a specific date and converts it to a csv file.
With the help [Pandas](http://pandas.pydata.org/) and
[MetPy](https://unidata.github.io/MetPy/latest/),
the data can be read, extended with new diagnostic variables
(CAPE, CIN, LCL, ...), and plotted in hodographs and skewplots.

## Usage

This repository consists of two main files:
- `soundings.py`: download and file I/O utilities
- `example.ipynb`: jupyter-notebook showing how to use the tool and compute
  further diagnostics

You can start the notebook directly in your browser (without python
installation!) via
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/acinn/soundings/master?filepath=example.ipynb)

## Installation

To use `Soundings` on your computer, the following libraries need to be installed:
- MetPy
- cartopy
- pandas
- numpy
- matplotlib

## Data source

[University of Wyoming](http://weather.uwyo.edu/upperair/sounding.html)

## Authors

Zora Schirmeister
