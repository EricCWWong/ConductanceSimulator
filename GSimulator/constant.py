import numpy as np

E_f = 10
h_bar = 1.05 * 10**(-34)  # 1.054571817 * 10**(-34)
e = 1.6 * 10 ** (-19)
m_e_eff = 10**(-31)
g = 1
mu_B = 5.79 * 10**(-2)    # 5.788 * 10 ** -5 eV

def get_fermi_energy():
    return float(E_f)

def get_h_bar():
    return float(h_bar)

def get_electron_charge():
    return float(e)

def get_electron_eff_mass():
    return float(m_e_eff)

def get_g():
    return float(g)

def get_mu_B():
    return float(mu_B)
    