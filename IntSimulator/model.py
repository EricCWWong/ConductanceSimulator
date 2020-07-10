from numpy import sqrt, exp, pi, absolute
from prettytable import PrettyTable
from .hamiltonians import total_hamiltonian
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


################################################################################
# Constants:
hbar = 1.05*10**(-34)
q = 1.6 * (10**(-19))
electron_mass = 9.1 * (10**(-31))
vacuum_permitivity = 8.85 * (10**(-12))


################################################################################
class Wire_Material:
    '''
        This is the wire material class. It stores the information of the 
        material where the 1D transport takes place. There is only one 
        constructor so we will specify parameters here.

    Parameters
    ----------
    dielec_cons: float
        This is the dielectric constant factor, where the exact dielectric
        constant of the material can be found by multiplying dielec_cons and
        the vacuum permitivitty. For example, GaAs has dielec_cons = 12.4, 
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
    '''

    def __init__(self, dielec_cons, conf_rng, eff_mass_e, name=None):
        self.dielec_cons = dielec_cons
        self.conf_rng = conf_rng
        self.eff_mass_e = eff_mass_e
        self.name = name

    def get_dielec_factor(self):
        '''
            This retrieve the dielec_cons value.
        '''

        return self.dielec_cons

    def get_eff_mass_factor(self):
        '''
            This retrieve the eff_mass_e value.
        '''

        return self.eff_mass_e

    def get_dielec_cons(self):
        '''
            This retrieve the exact value of the dielectric constant.
        '''

        return self.dielec_cons * vacuum_permitivity
    
    def get_conf_rng(self):
        '''
            This retrieve the confinement range of the material.
        '''

        return self.conf_rng

    def get_eff_mass_e(self):
        '''
            This retrieve the exact value of the effective mass of electron.
        '''

        return self.eff_mass_e * electron_mass

    def get_name(self):
        '''
            This retrieve the name of the material.
        '''

        return self.name


################################################################################
class Interacting_Model:
    '''
        This is the Model class. It stores the information of the whole a
        range of experiments through varying interaction. Since tehre are only 
        one constructor, we will specify parameter here.

    Parameters
    ----------
    wire_material: Wire_Material (class)
        This is the wire material class which includes the all the 
        essential information of our material in the experiments.
    no_of_elec: float
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
    '''

    def __init__(self, wire_material, no_of_elec, inter_rng, 
                int_increase=True, conf_increase=True):
        self.wire_material = wire_material
        self.inter_rng = inter_rng
        self.no_of_elec = no_of_elec
        self.int_incr = int_increase
        self.conf_incr = conf_increase

    def get_array(self, array_range, steps, reverse=False):
        '''
            This method helps us generate an array given a range 
            and number of steps.

        Parameters
        ----------
        array_rng: tuple (float, float)
            This is the range of the concerned array. The lower bound first.
        steps: int
            This is the number of steps we want from the generated array.
        reverse: bool (Optional)
            This indicates whether we want to reverse the array. Default is
            True.

        Returns
        -------
        output: numpy array
            After recieving the array range and number of steps, a numpy
            array is generated.
        '''

        if array_range[1] == array_range[0]:
            return np.full(steps, array_range[1])
        else:
            step_size = (array_range[1] - array_range[0])/steps

            output = np.arange(start=array_range[0],
                            stop=array_range[1],
                            step= step_size)
            
            if reverse is True:
                output = output[::-1]
            return output

    def print_result(self, pt_freq):
        '''
            This method generates the resulting energy levels of each
            experiment.

        Parameters
        ----------
        pt_freq: int
            This gives the number of experiments we want to conduct.

        Returns
        -------
        energies: array with 3 nested numpy array 
                i.e. array = [np.array, np.array, np.array]
            This array contains 3 numpy arrays corresponding to the ground 
            state, 1st excited state and the 2nd excited state energies.
            For example, energies[i][j] corresponds to the jth experiment
            of the ith energy level.
        x: array
            This corresponds to the ratio of interaction and confinement (V/t)
            for each experiment. 
        '''

        # Initialise table:
        table = PrettyTable()
        table.field_names = ['V_int (meV)', 'V_conf (meV)', 'V_int/V_conf ()',
                            'Electron Sep (nm)', 'Wire width (nm)', 'r_0 (nm)',
                            'E_g (meV)', 'E_1 (meV)', 'E_2 (meV)']

        # Set up the interaction strength and confinement strength:
        int_strength = self.get_array(self.inter_rng, pt_freq, self.int_incr)
        conf_strength = self.get_array(self.wire_material.get_conf_rng(),
                                    pt_freq, self.conf_incr)
        
        # Initialise arrays:
        x = []
        energy0 = []
        energy1 = []
        energy2 = []

        # Plotting and table printing:
        for i in tqdm.tqdm(range(pt_freq)):
            V = int_strength[i]
            t = conf_strength[i]
            H = total_hamiltonian(self.no_of_elec, t, V)

            E_g = H.eigenenergies()[0]
            E_1 = H.eigenenergies()[int(3**(self.no_of_elec) / 2)]
            E_2 = H.eigenenergies()[3**(self.no_of_elec) - 1]
            energy0.append(E_g)
            energy1.append(E_1)
            energy2.append(E_2)
            w = hbar/np.sqrt(self.wire_material.get_eff_mass_e() * t * q * 10**(-3)) * 10**(9)
            r_0 = (2 * q**(2) * hbar**(2) /(self.wire_material.get_dielec_cons() * self.wire_material.get_eff_mass_e()* (t*10**(-3) * q)**(2)))**(1/3) * 10**(9)
            if V == 0:
                r = 'No interaction'
            else:    
                r = q / (self.wire_material.get_dielec_cons() * 10**(-3) * V) * 10**(9)
            table.add_row([V, t, V/t, r, w, r_0, E_g, E_1, E_2])
            x.append(V/t)

        # Putting energies together as an array:
        energies = [energy0, energy1, energy2]

        # Output data table:
        ## Printing information on set-up:
        print("##########################################################")
        print("No. of experiment:", pt_freq)
        print("##########################################################")
        print("Material information:")
        if self.wire_material.get_name() is not None:
            print("Material         :", self.wire_material.get_name())
        print("- dielectric constant:", self.wire_material.get_dielec_factor(), "epsilon_0")
        print("- e- eff mass        :", self.wire_material.get_eff_mass_factor(), "m_e")
        print("##########################################################")
        print("")
        print("")

        ## Printing table:
        print(table)

        # return energies
        return energies, x


