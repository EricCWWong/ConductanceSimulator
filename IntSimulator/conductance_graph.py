from matplotlib import pyplot as plt
import numpy as np


"""
    The following section contains functions to plot the conductance plot
    when given energy of each energy level.
"""


def single_transmission(threshold_energy, x):
    """
        This function gives a single transmission on a conductance plot
        when given a threshold energy of an energy level. If the energy
        given in x is higher than the threshold energy, then there will
        be a 2e^2/h jump in conductance.

    Parameters
    ----------
    threshold_energy: float
        This is the energy required to reach a specific energy level.
    x : float
        This is the x-axis parameter of energy. For a given energy x,
        if x > threshold energy, then we will have a 2e^2/h jump in
        conductance.

    Returns
    -------
    t: float
        This is the transmission probability. If the energy, x, is above the
        threshold frequency, then the transmission will be 1.
        Otherwise, there will be no transmission.
    """

    # the transmission can be denoted as the Heaviside step function:
    t = 1/(1 + np.exp(-(x - threshold_energy)))
    return t


def total_transmission(energy_lvls, x):
    """
        This function gives the total transmission on a conductance plot
        when given threshold energies of all the concerned levels
        of the system.

    Parameters
    ----------
    energy_lvls: float array
        This is an array of energy of each energy levels of a
        particular system.
        First item (index [0]) in the array corresponds to the ground state
        of the system.
    x : float
        This is the x-axis parameter of energy. For a given energy x,
        if x > threshold energy of a certain level, then we will
        have a 2e^2/h jump in conductance.

    Returns
    -------
    output: float
        This is the total conductance of the whole system in units of 2e^2/h.
    """

    # We set the output for a certain energy x to be 0:
    output = 0

    # The conductance of a certain energy x can be calculated as
    # the sum of allowed transmission:
    for energy_lvl in energy_lvls:
        output = output + single_transmission(energy_lvl, x)
    return output


def conductance_plot(energies, offset):
    """
        This function plots the conductance curves when energy
        levels of the system in various set up is provided. It allows
        clear comparision between the conductance plot for different
        experimental setup. I plot is shown when the function is completed.

    Parameters
    ----------
    energies: float array
        This is a 2D array. For example, energies[i][j] corresponds
        to the energy of the ith level in the jth experiment.
    offset : float
        This is the distance between each conductance
        curve to allow each curve to be seen clearly.

    Returns
    -------
    None
    """

    no_channels = len(energies)
    no_curves = len(energies[0])

    # Initialise graphs:
    fig, axs = plt.subplots(1, 1)
    fig.suptitle('Conductance Plot')
    axs.set_ylabel('G (2e^2/h)')
    axs.set_xlabel('E (meV)')
    axs.set_ylim([0, no_channels])

    x = np.arange(-5, offset * no_curves + no_channels * 6, 0.1)

    for i in range(no_curves):
        energy_lvls = []
        for j in range(no_channels):
            energy_lvls.append(energies[j][i] - energies[0][i])
        y = total_transmission(energy_lvls, x - i* offset)

        axs.plot(x,y)

    plt.show()
        

