import matplotlib.pyplot as plt 
import numpy as np 
import math
from transmission import totalTransmission_n

n = 5       # Number of steps
V_sd = 0    # In units of h_bar w_x
B = 3
V_sd_steps = 5

# setting the x - coordinates 
x = np.arange(-10, 10, 0.1)    # In units of h_bar w_x



fig, axs = plt.subplots(1, 5)
fig.suptitle('The conductance of the material (1.5)')
axs[0].set_ylabel('G * h / 2e^2')
axs[int(V_sd_steps/2 -0.5)].set_xlabel('(E_f - U_0) / h_bar w_x')

for i in range (0, V_sd_steps):
    V_sd = i * 0.5
    # setting the corresponding y - coordinates
    y = 1/2 * totalTransmission_n(n, x, V_sd, B)
    axs[i].set_ylim([0, 5])
    #axs[i].set_xlim([-1, 10])   
    axs[i].plot(x,y)

  
# function to show the plot 
#plt.show()
plt.savefig('Conductance_with_Bfield2.pdf')
