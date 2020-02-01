import numpy as np
from argparse import ArgumentParser
from .model import Model
from .command_helper import read_setup, plotter
from .constant import Material


"""
This is the entry point file of the package GSimulator.
"""

def process():

    parser = ArgumentParser("Input the initial set up for the model (in .csv format):")

    parser.add_argument(
        'experiment_setup',
        action='store',
        help="This is csv file that contains the experiment set up.")

    parser.add_argument(
        'channels',
        action='store',
        help="Number of electron channels.")

    parser.add_argument(
        '--g',
        action='store',
        help="This is will be invoked if you would like to define the g factor of the \
             material. Default value is g = 0.04.")

    parser.add_argument(
        '--eff',
        action='store',
        help="This is will be invoked if you would like to define the effective mass of the \
             electrons in units of normal electron mass (m_e). Default value is 0.067*(m_e).")
    
    parser.add_argument(
        '--name',
        action='store',
        help="This will be invoked if you would like to name a specific material.")
    
    parser.add_argument(
        '--savefig',
        action='store',
        help="This will called if you would like to save your plot. The input will be the file name. \
            including the file format. Default fmt is .png.")

    arguments = parser.parse_args()

    if arguments.g is None:
        g = 0.04
    else:
        g = float(arguments.g)
    
    if arguments.eff is None:
        me_eff = 0.067
    else:
        me_eff = float(arguments.eff)

    # Constants
    exp_setup = read_setup(arguments.experiment_setup)
    channels = int(arguments.channels)
    material = Material(g, me_eff)

    # Printing information on set-up:
    print("######################################################")
    print("No. of experiment:", len(exp_setup))
    print("No. of channels  :", channels)
    print("######################################################")
    print("Material information:")
    if arguments.name is not None:
        name = arguments.name
        graphname = 'Conductance of ' + name
        print("Material         :", name)
    else:
        graphname = 'Conductance' 
    print("- Lande g-factor :", g)
    print("- e- eff mass    :", me_eff, "m_e")
    print("######################################################")

    savefig = arguments.savefig

    # Plot graph
    plotter(material, exp_setup, channels, graph_name=graphname, savefig=savefig)
    
if __name__ == "__main__":
    process()
