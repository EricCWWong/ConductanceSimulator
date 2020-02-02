import numpy as np


"""
This file includes all the important constant.
"""
  
class Material:
    def __init__(self, name="", g=0.04, me_eff=0.067):
        self.name = name
        self.m_e = 9.31 * 10 ** (-31)
        self.m_e_eff = me_eff * self.m_e
        self.g = g

h_bar = 1.05 * 10**(-34)  # 1.054571817 * 10**(-34)
e = 1.6 * 10 ** (-19)
mu_B = 5.79 * 10**(-2)    # 5.788 * 10 ** -5 eV