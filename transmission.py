import numpy as np 
import math

# rename variables
pi = np.pi

#

def transmissionForward (n, x, V_sd):
    return 1/(1 + np.exp(-2 * pi * (x - (2 * n + 1) + 1 / 2 * V_sd))) * 1 / 2

def transmissionBackward (n, x, V_sd):
    return 1/(1 + np.exp(-2 * pi * (x - (2 * n + 1) - 1 / 2 * V_sd))) * 1 / 2

def totalTransmission_n (n, x, V_sd):
    output = 0
    for i in range (0, n + 1):
        output = output + transmissionBackward(i, x, V_sd) + transmissionForward(i, x, V_sd)
    return output