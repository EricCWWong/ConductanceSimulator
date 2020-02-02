import numpy as np
from .model import Model
from matplotlib import pyplot as plt
from prettytable import PrettyTable


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

def read_material(file_name):
    """
    This will take a .csv file and retrieve the material information.

    Parameters
    ----------
    filename: str
        The filename that contains the material information in .csv format.

    Returns
    -------
    exp_setup: array
        This is the array for the material information.
    """

    material = np.genfromtxt(
        file_name,
        delimiter=",",
        names=True,
        dtype=['<U10', float, float])
    return material

def plotter(material, exp_setup, channels, offset, graph_name='conductance', fmt='pdf', savefig=None):
    """
    This will take in different experiment setup and plot the predicted graph.

    Parameters
    ----------
    material: object (Material)
        This object stores the data such as Lande g factor, effective electron
        mass for specific material.
    exp_setup: 2d-array
        The experiment setup, see the csv file format for details.
    channels: int
        The number of electrons channels taken into account.
    graph_name: str
        The name of the saved plot. Default is 'conductance'.
    fmt: str
        The format of the saved file.
    savefig: str
        The name of the fig if user wants it to be saved. If savefig is NONE, then 
        the figure will not be saved.

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

    # Initialise table:
    table = PrettyTable()
    table.field_names = ['hbar w_x (meV)', 'w_y/ w_x', 'B (T)', 'angle (rad)', 'E1 (meV)', 'E2 (meV)', 'eVsd (meV)', 'hbar w_c (meV)', 'Zeeman (meV)']
    
    # Setting up:
    plots = len(exp_setup)
    x = np.arange(-2, offset * plots + channels * 2, 0.1)

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

        # adding row data in table:
        table.add_row([model.hw_x, model.hw_y/model.hw_x, model.magnetic_field, model.angle, model.E1, model.E2, model.eVsd, model.hw_c, model.zeeman(1/2)])
        
        # calculate y values:
        y = model.total_transmission(channels, x - i * offset)
        axs.plot(x,y)

    print(table)

    if savefig is not None:
        file_name = savefig
        plt.savefig('./Results/' + file_name)
    plt.show()
