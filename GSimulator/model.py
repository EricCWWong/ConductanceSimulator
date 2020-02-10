import numpy as np
from numpy import pi, cos, exp, sqrt, radians
from .constant import h_bar, mu_B, Material


"""
This class stores all the required data of a certain experimental setup and perform
required calculations of the transmission rate.
"""

class Model:
    def __init__ (self, material, hw_x, hw_y, V_sd=0, magnetic_field=0, angle=0):
        
        # Basic ingredients:
        self.m = material
        self.hw_x = hw_x
        self.hw_y = hw_y
        self.eVsd = V_sd  # V_sd in mV ==> eV_sd in meV
        self.magnetic_field = magnetic_field
        self.angle = radians(angle)
        self.hw_c = h_bar * self.magnetic_field * cos(self.angle) / self.m.m_e_eff * 10**(3) # In terms of meV
        if np.abs(self.hw_c) < 0.00000001:
            self.hw_c = 0
        self.angular_freq = self.hw_c ** 2 + self.hw_y ** 2 - self.hw_x ** 2

        # Advanced ingredients:
        self.E1 = 1/(2 * pi * sqrt(2)) * (((self.angular_freq) ** 2 + 4 * (self.hw_x**2) * (self.hw_y**2))**(1/2) - self.angular_freq) ** (1/2)

        self.E2 = 1/(sqrt(2)) * (((self.angular_freq) ** 2 + 4 * (self.hw_x**2) * (self.hw_y**2))**(1/2) + self.angular_freq) ** (1/2)

    # Zeeman splitting term:
    def zeeman(self, S):
        """
        This will calculate the zeeman energy in corresponding spins.

        Parameters
        ----------
        S: float
            The spin of electrons.

        Returns
        -------
        zeeman_term: float
            Returns the calculated Zeeman term.
        """
        zeeman_term = self.m.g * mu_B * S * self.magnetic_field
        return zeeman_term

    # Transmission terms:
    def forward_transmission(self, n, x):
        """
        This will calculate the transmission rate of the forward travelling electrons.

        Parameters
        ----------
        n: int
            The nth channel.
        x: float
            The x value on the graph, in this case roughly proportional to Fermi energy.

        Returns
        -------
        t_forward: float
            Returns the forward transmission rate of the nth channel.
        """
        spin_up = 1/2
        spin_down = -1/2
        E1 = self.E1
        E2 = self.E2

        t_forward = 1/2 * 1/(1 + np.exp(-1/E1 * (self.hw_x * x + 1/2 * self.eVsd -(n + 1/2) * E2 + self.zeeman(spin_up)))) + \
            1/2 * 1/(1 + np.exp(-1/E1 * (self.hw_x * x + 1/2 * self.eVsd -(n + 1/2) * E2 + self.zeeman(spin_down))))
        return t_forward

    def backward_transmission(self, n, x):
        """
        This will calculate the transmission rate of the backward travelling electrons.

        Parameters
        ----------
        n: int
            The nth channel.
        x: float
            The x value on the graph, in this case roughly proportional to Fermi energy.

        Returns
        -------
        t_backward: float
            Returns the backward transmission rate of the nth channel.
        """

        spin_up = 1/2
        spin_down = -1/2
        E1 = self.E1
        E2 = self.E2

        t_backward = 1/2 * 1/(1 + np.exp(-1/E1 * (self.hw_x * x - 1/2 * self.eVsd -(n + 1/2) * E2 + self.zeeman(spin_up)))) + \
            1/2 * 1/(1 + np.exp(-1/E1 * (self.hw_x * x - 1/2 * self.eVsd -(n + 1/2) * E2 + self.zeeman(spin_down))))
        return t_backward

    def total_transmission(self, channels, x):
        """
        This will calculate the total transmission rate for all channels, calulated by
        summing all the individual channels.

        Parameters
        ----------
        channels: int
            The number of channels.
        x: float
            The x value on the graph, in this case roughly proportional to Fermi energy.

        Returns
        -------
        output: float
            Returns the total transmission rate of all channels.
        """

        output = 0
        for i in range (0, channels):
            output = output + self.forward_transmission(i, x) + self.backward_transmission(i, x)
        return output * 1/2