import numpy as np
from argparse import ArgumentParser
import matplotlib.pyplot as plt
from .model import Model
from .command_helper import read_setup, plotter


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
        '--constants',
        action='store',
        help="This is will be invoked if you would like to change the constants.")

    arguments = parser.parse_args()

    # Constants
    exp_setup = read_setup(arguments.experiment_setup)
    channels = int(arguments.channels)

    # Plot graph
    plotter(exp_setup, channels)
    
if __name__ == "__main__":
    process()
