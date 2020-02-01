import numpy as np
from .model import Model
import matplotlib.pyplot as plt


def read_setup(file_name):
    """
    This will take a .csv file and retrieve the experimental setup.

    Parameters
    ----------
    filename: str
        The filename that contains the experiment setup in .csv format.

    Returns
    -------
    exp_setup: array
        This is the array for experiment setup.
    """

    exp_setup = np.genfromtxt(
        file_name,
        delimiter=",",
        skip_header=1)
    if exp_setup.ndim == 1:
        exp_setup = [exp_setup]
        exp_setup = np.array(exp_setup)
    return exp_setup

def plotter(material, exp_setup, channels, graph_name='conductance', fmt='pdf', savefig=None):
    """
    This will take in different experiment setup and plot the predicted graph.

    Parameters
    ----------
    exp_setup: 2d-array
        The experiment setup, see the csv file format for details.
    channels: int
        The number of electrons channels taken into account.
    graph_name: str
        The name of the saved plot. Default is 'conductance'.
    fmt: str
        The format of the saved file.

    Returns
    -------
    The required plot.
    """

    # Initialise graph:
    fig, axs = plt.subplots(1, 1)
    fig.suptitle(graph_name)
    axs.set_ylabel(r'$G \times \frac{h}{2e^{2}} $')
    axs.set_xlabel(r'$ \frac{E_{f} - U_{0}}{\hbar w_{x}}$')
    axs.set_ylim([0, channels])
    
    # Setting up:
    plots = len(exp_setup)
    x = np.arange(-2, 2 * plots + channels * 2, 0.1)

    for i in range(plots):
        # initialise experiment setup:
        experiment = exp_setup[i]
        hw_x = experiment[0]
        hw_y = experiment[1] * hw_x
        V_sd = experiment[2]
        B = experiment[3]
        angle = experiment[4]

        # constructing model:
        model = Model(material, hw_x, hw_y, V_sd, B, angle)
        
        # calculate y values:
        y = model.total_transmission(channels, x - i * 2)
        axs.plot(x,y)

    if savefig is not None:
        file_name = savefig
        plt.savefig('./Results/' + file_name)
    plt.show()