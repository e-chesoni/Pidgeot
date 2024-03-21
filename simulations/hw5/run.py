import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import minimize_scalar

from util.uav_logger import *
from simulations.hw5.setup import *

def run_hw5_simulation():
    logging.info("running HW5 simulation...\n")

    # Set degree of polynomial
    poly_degree = 2  # NOTE: use 2 for quadratic, 3 for cubic (life = harder if you use cubic)

    # Fit polynomial to CT vs J
    coeffs_ct = np.polyfit(df_1['J'], df_1['CT'], poly_degree)
    # Generate a polynomial function from the coefficients
    poly_ct = np.poly1d(coeffs_ct)

    # Fit a polynomial to CP vs J
    coeffs_cp = np.polyfit(df_1['J'], df_1['CP'], poly_degree)
    poly_cp = np.poly1d(coeffs_cp)

    # Generate points to plot the fitted polynomial curves
    J_new = np.linspace(min(df_1['J']), max(df_1['J']), 500)  # NOTE: add  more points for a smoother curve
    CT_fit = poly_ct(J_new)
    CP_fit = poly_cp(J_new)

    # Plotting
    plt.figure(figsize=(12, 6))

    # CT vs J with polynomial fit
    plt.subplot(1, 2, 1)
    plt.plot(df_1['J'], df_1['CT'], 'o', label='Original Data')
    plt.plot(J_new, CT_fit, '-', label=f'{poly_degree} Degree Polynomial Fit')
    plt.title('CT vs J with Polynomial Fit')
    plt.xlabel('J')
    plt.ylabel('CT')
    plt.legend()

    # CP vs J with polynomial fit
    plt.subplot(1, 2, 2)
    plt.plot(df_1['J'], df_1['CP'], 'x', label='Original Data')
    plt.plot(J_new, CP_fit, '--', label=f'{poly_degree} Degree Polynomial Fit')
    plt.title('CP vs J with Polynomial Fit')
    plt.xlabel('J')
    plt.ylabel('CP')
    plt.legend()

    plt.tight_layout()
    plt.show()
