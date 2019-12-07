import numpy as np 
import math

# rename variables
pi = np.pi


def zeemanEnergy (S, B):
    g = 1
    mu_B = 1
    return g * mu_B * S * B


# transmission coefficients without B field

def transmissionForward (n, x, V_sd, B = 0, S = 1/2):
    return 1/(1 + np.exp(-2 * pi * (x - (2 * n + 1) + 1 / 2 * V_sd + zeemanEnergy(1/2, 1)))) * 1 / 2

def transmissionBackward (n, x, V_sd, B = 0, S = 1/2):
    return 1/(1 + np.exp(-2 * pi * (x - (2 * n + 1) - 1 / 2 * V_sd + zeemanEnergy(1/2, 1)))) * 1 / 2

def totalTransmission_n (n, x, V_sd, B = 0):
    output = 0
    for i in range (0, n + 1):
        output = output + transmissionBackward(i, x, V_sd) + transmissionForward(i, x, V_sd)
    return output
