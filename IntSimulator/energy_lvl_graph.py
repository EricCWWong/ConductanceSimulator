from numpy import sqrt, exp, pi, absolute
from matplotlib import pyplot as plt
import numpy as np
import tqdm


def energy_level_plot(energies, Vt_ratio):
    '''
        This function plots the energy level curves when energy levels of the
        system in various set up is provided. It allows clear comparision 
        between the energy levels. A plot is shown when the
        function is completed.

    Parameters
    ----------
    energies: float array
        This is a 2D array. For example, energies[i][j] corresponds to the 
        energy of the ith level in the jth experiment.
    V/t_ratio : array 
        This is the array containing the ratio of interaction and confinement
        in each experiment.

    Returns
    -------
    None
    '''

    # Initialise graphs:
    fig, axs = plt.subplots(1, 1)
    fig.suptitle('Subbands energy')
    axs.set_ylabel('E (meV)')
    axs.set_xlabel('V/t')

    # Finalise plot:
    for i, energy in enumerate(energies):
        energy = np.array(energy)
        if i == 0:
            lab = 'ground state'
        else:
            lab = 'excited state ' + str(i)
        axs.plot(Vt_ratio, energy, label=lab)

    plt.legend(loc="upper left")

    plt.show()

def energy_gap_plot(energies, Vt_ratio):
    '''
        This function plots shows the energy gap of the ground state and
        the first excited state.

    Parameters
    ----------
    energies: float array
        This is a 2D array. For example, energies[i][j] corresponds to the 
        energy of the ith level in the jth experiment.
    V/t_ratio : array 
        This is the array containing the ratio of interaction and confinement
        in each experiment.

    Returns
    -------
    None
    '''

    # Initialise graphs:
    fig, axs = plt.subplots(1, 1)
    fig.suptitle('Energy gap between ground and 1st excited state')
    axs.set_ylabel('\delta E (meV)')
    axs.set_xlabel('V/t')

    # Calculate energy gap:
    energy0 = np.array(energies[0])
    energy1 = np.array(energies[1])
    energy_gap = energy1 - energy0
    axs.plot(Vt_ratio, energy_gap)

    # Show plot
    plt.show()