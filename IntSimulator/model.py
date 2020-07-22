from numpy import sqrt, exp, pi, absolute
from prettytable import PrettyTable
from .hamiltonians import total_hamiltonian, hamiltonian_site_i
from .model_helper import get_array
from qutip import tensor, Qobj
import numpy as np
import tqdm

'''
    !!!Dependencies:
        In this file, apart from the usual numpy class, tqdm and 
        prettytable is required.

    Description:
    This file contains classes that forms the quantum wire model.
    This includes the wire material class and the model class.
    Some important constants are also included in this file.
'''

##############################################################################
# Constants:
hbar = 1.05 * 10 ** (-34)
q = 1.6 * (10 ** (-19))
electron_mass = 9.1 * (10 ** (-31))
vacuum_permittivity = 8.85 * (10 ** (-12))


##############################################################################


class WireMaterial:
    """
        This is the wire material class. It stores the information of the
        material where the 1D transport takes place. There is only one
        constructor so we will specify parameters here.

    Parameters
    ----------
    dielec_cons: float
        This is the dielectric constant factor, where the exact dielectric
        constant of the material can be found by multiplying dielec_cons and
        the vacuum permittivity. For example, GaAs has dielec_cons = 12.4,
        vacuum has dielec_cons = 1.
    conf_rng: tuple (float, float)
        This is a tuple containing the confinement energy range with units
        meV. To give constant confinement, simply fix both the upper bound
        and lower bound the same value.
    eff_mass_e: float
        This is the effective mass factor, where the exact effective mass
        equals to eff_mass_e multiply by electron rest mass.
    name: str (Optional)
        This is the name of the material. It is an optional parameter.
    """

    def __init__(self, dielec_cons, conf_rng, eff_mass_e, name=None):
        self.dielec_cons = dielec_cons
        self.conf_rng = conf_rng
        self.eff_mass_e = eff_mass_e
        self.name = name

    def get_dielec_factor(self):
        """
            This retrieve the dielec_cons value.
        """

        return self.dielec_cons

    def get_eff_mass_factor(self):
        """
            This retrieve the eff_mass_e value.
        """

        return self.eff_mass_e

    def get_dielec_cons(self):
        """
            This retrieve the exact value of the dielectric constant.
        """

        return self.dielec_cons * vacuum_permittivity

    def get_conf_rng(self):
        """
            This retrieve the confinement range of the material.
        """

        return self.conf_rng

    def get_eff_mass_e(self):
        """
            This retrieve the exact value of the effective mass of electron.
        """

        return self.eff_mass_e * electron_mass

    def get_name(self):
        """
            This retrieve the name of the material.
        """

        return self.name


##############################################################################
class InteractingModel:
    """
        This is the Model class. It stores the information of the whole a
        range of experiments through varying interaction. Since there are only
        one constructor, we will specify parameter here.

    Parameters
    ----------
    wire_material: WireMaterial (class)
        This is the wire material class which includes the all the
        essential information of our material in the experiments.
    no_of_elec: int
        This is the number of electrons in the whole system simulated.
    inter_rng: tuple (float, float)
        This is the range of interaction energy in units of meV. To give
        constant interaction, simply fix both the upper bound and lower
        bound the same value.
    int_increase: bool (Optional)
        This indicates whether the interaction strength will increase
        each experiment.
    conf_increase: bool (Optional)
        This indicates whether the confinement strength will increase
        each experiment.
    """

    def __init__(self, wire_material, no_of_elec, inter_rng,
                 int_increase=True, conf_increase=True):
        self.wire_material = wire_material
        self.inter_rng = inter_rng
        self.no_of_elec = no_of_elec
        self.int_incr = int_increase
        self.conf_incr = conf_increase

    def get_1st_excited(self):
        h_site_j = hamiltonian_site_i(1)
        first_ex_state = h_site_j.eigenstates()[1][1]
        full_state = []
        for i in range(self.no_of_elec):
            full_state.append(first_ex_state)
        full_state = tensor(full_state).data
        full_state = Qobj(full_state)
        return full_state

    def print_result(self, pt_freq, include_2nd=False):
        """
            This method generates the resulting energy levels of each
            experiment.

        Parameters
        ----------
        pt_freq: int
            This gives the number of experiments we want to conduct.
        include_2nd: bool
            This denotes whether to include the 2nd excited state in the
            energy band diagram.

        Returns
        -------
        energies: array with 3 nested numpy array
                i.e. array = [np.array, np.array, np.array]
            This array contains 3 numpy arrays corresponding to the ground
            state, 1st excited state and the 2nd excited state energies.
            For example, energies[i][j] corresponds to the jth experiment
            of the ith energy level.
        x: array
            This corresponds to the ratio of interaction and confinement (v/t)
            for each experiment.
        """

        # Initialise table:
        table = PrettyTable()
        table.field_names = ['V_int (meV)', 'V_conf (meV)', 'V_int/V_conf ()',
                             'Electron Sep (nm)', 'Wire width (nm)',
                             'r_0 (nm)', 'e_g (meV)', 'e_1 (meV)',
                             'e_2 (meV)']

        # Set up the interaction strength and confinement strength:
        int_strength = get_array(self.inter_rng, pt_freq, self.int_incr)
        conf_strength = get_array(self.wire_material.get_conf_rng(),
                                  pt_freq, self.conf_incr)

        # Initialise arrays:
        x = []
        energy0 = []
        energy1 = []
        energy2 = []

        # Initial first excited state (without interaction):
        first_ex_state = self.get_1st_excited()

        # Plotting and table printing:
        for i in tqdm.tqdm(range(pt_freq)):
            # Retrieving energies strength and Hamiltonian:
            v = int_strength[i]
            t = conf_strength[i]
            h = total_hamiltonian(self.no_of_elec, t, v)

            # Calculate and retrieve the eigenstates and its
            # corresponding energies:
            eigenstates = h.eigenstates()
            eigenenergies = eigenstates[0]
            eigenstates = eigenstates[1]

            # The ground state and the 2nd excited state are trivial:
            e_g = eigenenergies[0]
            e_2 = eigenenergies[3 ** self.no_of_elec - 1]

            # Calculating the  1st excited state:
            # If i is 0, we know that there are no interactions
            # and the energy is 3/2 Nt:
            if i == 0:
                e_1 = 3 / 2 * self.no_of_elec * t
            # Otherwise, we need to compare the new states with the
            # previous chosen state and choose the new state as one with
            # most overlapping with the old one:
            else:
                # Calculating the magnitude of the overlapping:
                max_overlap = abs(eigenstates[1].overlap(first_ex_state))
                max_overlap_index = 1  # Setting the initial index:
                for j in range(2, 3 ** self.no_of_elec - 1):
                    overlap = abs(eigenstates[j].overlap(first_ex_state))

                    # If there are more overlapping, we replace this as the
                    # new chosen state:
                    if overlap > max_overlap:
                        max_overlap = overlap
                        max_overlap_index = j

                # Setting the final chosen eigenstate:
                e_1 = eigenenergies[max_overlap_index]
                first_ex_state = eigenstates[max_overlap_index]

            # Storing the data of the 3 important energies:
            energy0.append(e_g)
            energy1.append(e_1)
            energy2.append(e_2)

            # Calculating the wire width:
            w = hbar / np.sqrt(
                self.wire_material.get_eff_mass_e()
                * t * q * 10 ** (-3)) * 10 ** 9

            # Calculating the interesting length scale, r0:
            r_0 = (2 * q ** 2 * hbar ** 2 / (
                    self.wire_material.get_dielec_cons()
                    * self.wire_material.get_eff_mass_e() *
                    (t * 10 ** (-3) * q) ** 2)) ** (1 / 3) * 10 ** 9

            # Calculating electrons separation:
            if v == 0:
                r = 'No interaction'
            else:
                r = q / (self.wire_material.get_dielec_cons()
                         * 10 ** (-3) * v) * 10 ** 9

            # Update table:
            table.add_row([v, t, v / t, r, w, r_0, e_g, e_1, e_2])

            # Update independent variable, ratio of int and conf:
            x.append(v / t)

        # Putting energies together as an array:
        energies = [energy0, energy1]

        if include_2nd is True:
            energies.append(energy2)

        # Output data table:
        # Printing information on set-up:
        print("##########################################################")
        print("No. of experiment:", pt_freq)
        print("##########################################################")
        print("Material information:")
        if self.wire_material.get_name() is not None:
            print("Material         :", self.wire_material.get_name())
        print("- dielectric constant:",
              self.wire_material.get_dielec_factor(), "epsilon_0")
        print("- e- eff mass        :",
              self.wire_material.get_eff_mass_factor(), "m_e")
        print("##########################################################")
        print("")
        print("")

        # Printing table:
        print(table)

        # return energies
        return energies, x
