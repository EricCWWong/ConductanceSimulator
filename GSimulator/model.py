import numpy as np
from constant import get_fermi_energy, get_h_bar, get_electron_charge, get_electron_eff_mass, get_g, get_mu_B


class Model:
    def __init__ (self, w_x, w_y, V_sd=0, magnetic_field=0, angle=0):
        self.w_x = w_x
        self.w_y = w_y
        self.V_sd = V_sd
        self.magnetic_field = magnetic_field
        self.angle = angle
        self.e = get_electron_charge()
        self.m_e_eff = get_electron_eff_mass()
        self.w_c = self.e * magnetic_field * np.cos(angle) / (self.m_e_eff)
        self.angular_freq = self.w_c ** 2 + self.w_y ** 2 - self.w_x ** 2

    def set_Vsd(self, new_V_sd):
        self.V_sd = new_V_sd

    def set_magnetic(self, new_B):
        self.magnetic_field = new_B

    def set_angle(self, new_angle):
        self.angle = new_angle

    def get_Vsd(self):
        return self.V_sd

    def get_magnetic(self):
        return self.magnetic_field

    def get_angle(self):
        return self.angle

    def get_E1(self):
        # constants...
        h_bar = get_h_bar()
        w_x = self.w_x
        w_y = self.w_y
        angular_freq = self.angular_freq

        E1 = h_bar/(2 * np.pi * np.sqrt(2)) * (((angular_freq) ** 2 + 4 * (w_x**2) * (w_y**2))**(1/2) - angular_freq) ** (1/2)

        return float(E1)

    def get_E2(self):
        # constants...
        h_bar = get_h_bar()
        w_x = self.w_x
        w_y = self.w_y
        angular_freq = self.angular_freq

        E2 = h_bar/(np.sqrt(2)) * (((angular_freq) ** 2 + 4 * (w_x**2) * (w_y**2))**(1/2) + angular_freq) ** (1/2)

        return float(E2)

    def get_zeeman(self, S):
        # constants...
        g = get_g()
        mu_B = get_mu_B()

        return g * mu_B * S * self.magnetic_field

    def forward_transmission(self, n, x):
        spin_up = 1/2
        spin_down = -1/2
        h_bar = get_h_bar()
        w_x = self.w_x
        e = self.e
        V_sd = self.V_sd

        E1 = self.get_E1()
        E2 = self.get_E2()

        t_forward = 1/2 * 1/(1 + np.exp(-1/E1 * (h_bar * w_x * x + 1/2 * e * V_sd -(n + 1/2) * E2 + self.get_zeeman(spin_up)))) + \
            1/2 * 1/(1 + np.exp(-1/E1 * (h_bar * w_x * x + 1/2 * e * V_sd -(n + 1/2) * E2 + self.get_zeeman(spin_down))))

        return t_forward

    def backward_transmission(self, n, x):
        spin_up = 1/2
        spin_down = -1/2
        h_bar = get_h_bar()
        w_x = self.w_x
        e = self.e
        V_sd = self.V_sd

        E1 = self.get_E1()
        E2 = self.get_E2()

        t_back = 1/2 * 1/(1 + np.exp(-1/E1 * (h_bar * w_x * x - 1/2 * e * V_sd -(n + 1/2) * E2 + self.get_zeeman(spin_up)))) + \
            1/2 * 1/(1 + np.exp(-1/E1 * (h_bar * w_x * x - 1/2 * e * V_sd -(n + 1/2) * E2 + self.get_zeeman(spin_down))))

        return t_back

    def total_transmission(self, channels, x):
        output = 0
        for i in range (0, channels + 1):
            output = output + self.forward_transmission(i, x) + self.backward_transmission(i, x)
        return output * 1/2