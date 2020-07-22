from qutip import basis, Qobj, qeye, tensor, qdiags
from numpy import sqrt, exp, pi, absolute
from matplotlib import pyplot as plt
import numpy as np
import tqdm


'''
    !!!Dependencies:
        In this file, we have chosen to use the Qutip module to perform
        eigenstate and eigenenergies calculations.

    Description:
    This file consists of the Hamiltonian's of the 3 site model proposed
    in Bose's paper.
'''

# we define a 3x3 identity:
identity_3 = qeye(3)


# Hamiltonian (single site)...
def hamiltonian_site_i(t):
    """
        This function gives the single site Hamiltonian with confinement
        energy t. This confinement is modeled as a Harmonic oscillator.

    Parameters
    ----------
    t: float
        This is the confinement energy. It is in unit meV.

    Returns
    -------
    H_site: Qobj
        This returns a 3x3 matrix representing the single site Hamiltonian.
        In particular, since this is modelling the Harmonic oscillator,
        we have eigenenergies: (n+1/2)*t where t is the confinement.
    """

    t = float(t)

    H_site = Qobj([[3/2, -np.sqrt(2)/2,0],
                [-np.sqrt(2)/2, 3/2, -np.sqrt(2)/2],
                [0, -np.sqrt(2)/2, 3/2]])*(t)
    return H_site


def hamiltonian_site(no_of_elec, concerned_site, t):
    """
        This function gives the single site Hamiltonian with confinement
        energy t in a N electron model. This confinement is modeled as a
        Harmonic oscillator. We have added tensor products between particles
        to account for it in a N electron model.

    Parameters
    ----------
    no_of_elec: int
        This is the number of electrons in the whole system.
    concerned_site: int
        This is the site where we will like to add the confinement
        Hamiltonian.
    t: float
        The confinement energy. It is in units of meV.

    Returns
    -------
    H_site: Qobj
        This returns a 3^N x 3^N matrix representing the single site
        Hamiltonian in an N particle system. In particular, since this
        is modelling the Harmonic oscillator, we have eigenenergies:
        (n+1/2)*t where t is the confinement.
    """
    
    H = []
    for i in range(no_of_elec):
        if i == concerned_site:
            H.append(hamiltonian_site_i(t))
        else:
            H.append(identity_3)

    H_site = tensor(H).data
    
    return Qobj(H_site)


def total_hamiltonian_site(no_of_elec, t):
    """
        This function gives the total Hamiltonian with all the sites with a
        confinement.

    Parameters
    ----------
    no_of_elec: int
        This is the number of electrons in the whole system.
    t: float
        The confinement energy. It is in units of meV.

    Returns
    -------
    H_site: Qobj
        This returns a 3^N x 3^N matrix representing the single
        site Hamiltonian in an N particle system. In particular,
        since this is modelling N Harmonic oscillator, we have eigenenergies:
        (n+1/2)*N*t where t is the confinement.
    """

    H = 0
    for i in range(no_of_elec):
        H = H + hamiltonian_site(no_of_elec, i, t)
    return H


# Hamiltonian (interaction)...
def hamiltonian_int_i(V):
    """
        This function gives the Hamiltonian of 2 interacting electrons with
        interaction strength V.

    Parameters
    ----------
    V: float
        The interaction strength between electrons in units of meV.

    Returns
    -------
    H_site: Qobj
        This returns a 9 x 9 matrix representing a single interaction
        between electrons.
    """
    V = float(V)
    return qdiags([V,V/sqrt(2),V/sqrt(5),
                V/sqrt(2),V,V/sqrt(2),
                V/sqrt(5),V/sqrt(2),V], 0)


def hamiltonian_int(no_of_elec, concerned_site, V):
    """
        This function gives Hamiltonian of a single interaction between two
        electrons withinteraction strength V in an N particle system.

    Parameters
    ----------
    no_of_elec: int
        This is the number of electrons in the whole system.
    concerned_site: int
        This is the site where we will like to interact with the next
        electrons.
        For example, if concerned site = i then it interacts with the (i+1)th
        electron.
    V: float
        The interaction strength between electrons in units of meV.

    Returns
    -------
    H_site: Qobj
        This returns a 3^N x 3^N matrix representing a single interaction
        between 2 concerned electrons in an N electrons system.
    """

    H = []
    for i in range(no_of_elec-1):
        if i == concerned_site:
            H.append(hamiltonian_int_i(V))
        else:
            H.append(identity_3)

    H_int = tensor(H).data

    return Qobj(H_int)


def total_hamiltonian_int(no_of_elec, V):
    """
        This function gives total Hamiltonian of a N particle system where
        all N electrons are interacting with its neighbour electrons.

    Parameters
    ----------
    no_of_elec: int
        This is the number of electrons in the whole system.
    V: float
        The interaction strength between electrons in units of meV.

    Returns
    -------
    H_site: Qobj
        This returns a 3^N x 3^N matrix representing a single interaction
        between electrons.
    """

    H = 0
    for i in range(no_of_elec - 1):
        H = hamiltonian_int(no_of_elec, i, V)
    return H


# total Hamiltonian...
def total_hamiltonian(no_of_elec, t, V):
    """
        This function gives total Hamiltonian of a N particle system where
        both interaction and confinement is included.

    Parameters
    ----------
    no_of_elec: int
        This is the number of electrons in the whole system.
    t: float
        The confinement energy. It is in units of meV.
    V: float
        The interaction strength between electrons in units of meV.

    Returns
    -------
    H_site: Qobj
        This returns a 3^N x 3^N matrix representing the total Hamiltonian.
    """

    H = total_hamiltonian_site(no_of_elec, t) + \
        total_hamiltonian_int(no_of_elec, V)
    return H
