import numpy as np
from argparse import ArgumentParser
from .model import Model
from .command_helper import read_setup, plotter, read_material
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
        '--material',
        action='store',
        help="This is will be invoked if you would like to define the g factor of the \
             material. Default value is g = 0.04.")
    
    parser.add_argument(
        '--gname',
        action='store',
        help="This is will be name of the plot.")

    parser.add_argument(
        '--save',
        action='store',
        help="This will called if you would like to save your plot. The input will be the file name. \
            including the file format. Default fmt is .png.")
    
    parser.add_argument(
        '--offset',
        action='store',
        help="The translation of the curves, in units of meV.")

    arguments = parser.parse_args()

    if arguments.material is None:
        name = ''
        g = 0.04
        me_eff = 1
    else:
        mat_info = read_material(arguments.material)
        name = mat_info['Name']
        g = mat_info['g']
        me_eff = mat_info['m_eff']

    
    if arguments.offset is None:
        offset = 2
    else:
        offset = float(arguments.offset)

    # Constants
    exp_setup = read_setup(arguments.experiment_setup)
    channels = int(arguments.channels)
    material = Material(name, g, me_eff)
    graphname = arguments.gname

    # Printing information on set-up:
    print("######################################################")
    print("No. of experiment:", len(exp_setup))
    print("No. of channels  :", channels)
    print("######################################################")
    print("Material information:")
    if name != '':
        print("Material         :", name)
    print("- Lande g-factor :", g)
    print("- e- eff mass    :", me_eff, "m_e")
    print("######################################################")
    print("")
    print("")
    print("Graph Name:", graphname)

    savefig = arguments.save

    # Plot graph
    plotter(material, exp_setup, channels, offset, graph_name=graphname, savefig=savefig)
    
if __name__ == "__main__":
    process()
