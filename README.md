# GSimulator
This package allows user to plot the conductance graph of a quantum wire. There are main feature of this package 1)We have a command line operated simulation on 
non-interacting quantum wires, see Usage section for more detail. 2)A simulation in the interacting regime is also included. However, unlike the non-interacting case,
it doesn't currently have features to be used purely in command-line. All model classes and plotting functions can be imported in python files once installed.

It is tested to run on Linux platform. 

## Installation

Before running, ensure `pip` is installed. It can be installed by:

```
$ sudo apt install python3-pip
```

Browse the directory where the setup.py file lives and run:

```
$ pip install .
```
if permission is required, run:

```
$ pip install --user .
```

## Usage (Command Line)

We allow users to use the package in command line settings. This can be done by using the word `gsimulator` as shown below:

```
$ gsimulator exp_setup.csv 5 --material material.csv --gname 'G with g=2' --save 'filename.pdf' --offset 2
```
where exp_setup.csv and channels holds the information of the experiment and the number of channels involved respectively. material.csv holds all the information that is material dependent, such as name of material, effective mass of electrons, and the Lande g factor. `--gname` allows you to choose what you want the plot to be named, and `--save` allows you to save the graph with appropriate name. Note that a file type will be specified with the name, if no file type is given, the saved plot will be in .png format. If no inputs are given to `--save`, the graphs will not be saved. Last but not least, `--offset` allows you to chose how far each graph is seperated.

To make it simpler to use, I have also included 2 bash files, `run.sh` and `run_save.sh` in the example file. The first one will only create the plot and the data table in the the terminal, while the `run_save.sh` will save the plot and the terminal output to a directory called Result that you have to create. If you would like to change the data csv files, material csv files, channels, graph name, file name and offset, simply open these .sh files with notepad, text editor and change the input according to the above rules.

To execute the `run.sh` file, simply type:

```
$ ./run.sh
```

Similarly for `run_save.sh` file.

For more information, type in terminal:

```
$ gsimulator --help
```

Examples of the .csv files are also located in the Example file.

## Usage (Python Programming)
To import the modules or functions for non-interacting simulation, we simply type:

```
import GSimulator
```

Similarly, to import modules or functions for interacting simulation, we simply type:

```
import IntSimulator
```

