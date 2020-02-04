# GSimulator
This package allows user to plot the conductance graph of a quantum wire.

## Installation

Browse the directory where the setup.py file lives and run:

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
$ gsimulator exp_setup.csv 5 --material material.csv --gname 'G with g=2' --save 'filename.pdf' --offset 2
```
where exp_setup.csv and channels holds the information of the experiment and the number of channels involved respectively. material.csv holds all the information that is material dependent, such as name of material, effective mass of electrons, and the Lande g factor. `--gname` allows you to choose what you want the plot to be named, and `--save` allows you to save the graph with appropriate name. Note that a file type will be specified with the name, if no file type is given, the saved plot will be in .png format. If no inputs are given to `--save`, the graphs will not be saved. Last but not least, `--offset` allows you to chhose how far each graph is seperated.

To make it simpler to use, I have also included 2 bash files, `run.sh` and `run_save.sh`. The first one will only create the plot and the data table in the the terminal, while the `run_save.sh` will save the plot and the terminal output. If you would like to change the data files, material files, channels, graph name, file name and offset, simply open these .sh files with notepad, text editor and change the input according to the above rules.

For more information, type in terminal:

```
$ gsimulator --help
```

