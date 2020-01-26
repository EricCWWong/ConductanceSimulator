import numpy as np
from model import Model
import matplotlib.pyplot as plt

def single_plot(model, channels, graph_name='unnamed', fmt='pdf'):
    x = np.arange(-2, 10, 0.1)
    y = model.total_transmission(channels, x)

    fig, axs = plt.subplots(1, 1)
    fig.suptitle(graph_name)

    axs.set_ylabel(r'$G \times \frac{h}{2e^{2}} $')
    axs.set_xlabel(r'$ \frac{E_{f} - U_{0}}{\hbar w_{x}}$')

    axs.plot(x,y)

    axs.set_ylim([0, 5])   

    file_name = graph_name + '.' + fmt

    plt.savefig(file_name)
    plt.show()

def plot_comparison(
    model, channels, plots, indep_var, increment, space=2,
    graph_name='unnamed', fmt='pdf'):

    Vsd_init = model.get_Vsd()
    B_init = model.get_magnetic()

    fig, axs = plt.subplots(1, 1)
    fig.suptitle(graph_name)

    axs.set_ylabel(r'$G \times \frac{h}{2e^{2}} $')
    axs.set_xlabel(r'$ \frac{E_{f} - U_{0}}{\hbar w_{x}}$')
    axs.set_ylim([0, 5])  

    x = np.arange(-2, 20, 0.01)

    for i in range(plots):
        if indep_var == 'V':
            model.set_Vsd(Vsd_init + i*increment)
        elif indep_var == 'B':
            model.set_magnetic(B_init + i*increment)

        y = model.total_transmission(channels, x - i*space)
        axs.plot(x,y)

    file_name = graph_name + '.' + fmt

    plt.savefig(file_name)
    plt.show()


