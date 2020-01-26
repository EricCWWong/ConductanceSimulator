import numpy as np
import matplotlib.pyplot as plt
from model import Model
from constant import get_h_bar, get_electron_charge
from plotter import single_plot, plot_comparison
import sys


def process():
    # Constants
    e = get_electron_charge()
    h_bar = get_h_bar()
    w_x = 1 / h_bar # in terms of meV
    w_y = 2 * w_x
    V_sd_unit = h_bar * w_x / e
    B = 17
    angle = 1

    # Steps
    plots = 6
    channels = 5
    V_sd = 0 * V_sd_unit
    steps = 2 * V_sd_unit

    model = Model(w_x, w_y, V_sd, B, angle)

    single_plot(model, channels, 'test')

    plot_comparison(model, channels, plots, 'V', steps, 2, 'test2')

if __name__ == "__main__":
    process()
