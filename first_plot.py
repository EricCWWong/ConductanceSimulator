import matplotlib.pyplot as plt 
import numpy as np 
import math
from transmission import totalTransmission_n

n = 5       # Number of steps
V_sd = 0    # In units of h_bar w_x

# setting the x - coordinates 
x = np.arange(-1, 10, 0.1)    # In units of h_bar w_x



fig, axs = plt.subplots(1, 5)
fig.suptitle('The conductance of the material with a V_sd but no magnetic field')
axs[0].set_ylabel('G * h / 2e^2')
axs[2].set_xlabel('(E_f - U_0) / h_bar w_x')

for i in range (0, 5):
    V_sd = i * 0.5
    # setting the corresponding y - coordinates
    y = totalTransmission_n(n, x, V_sd)
    axs[i].set_ylim([0, 5])
    #axs[i].set_xlim([-1, 10])
    
    axs[i].plot(x,y)

  
# function to show the plot 
plt.savefig('Conductance_without_B_field.pdf')
