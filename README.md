# GSimulator
This package allows user to plot the conductance graph of a quantum wire.

## Installation

Browse the directory where the file lives and run:

```
pip install .
```
if permission is required, run:

```
pip install --user .
```

## Usage

We allow users to use the package in command line settings. This can be done by using the word `gsimulator` as shown below:

```
$ gsimulator exp_setup.csv channels [--constants CONSTANTS.csv]
```

where exp_setup.csv and channels holds the information of the experiment and the number of channels involved respectively. To change the constants values, you will need to parse in --constants const_file.csv where this .csv file holds the constants. Suppose we have AlGaAs.csv as the constant file:

```
$ gsimulator exp_setup.csv channels --constants AlGaAs.csv
```

By default it will generate the required graphs and saved the plots automatically.

For more information, type in terminal:

```
$ gsimulator --help
```
