import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.optimize import curve_fit

from util.uav_logger import *
from util.helpers import *
from src.simulate import *
from src.setup import *
from src.aircraft import *
from simulations.hw4.setup import *


# Set DEBUG option
DEBUG = True

# PROBLEM 1
# WING
super_cub_wing = Wing()
super_cub_wing.set_span_m(wing_span_m)
super_cub_wing.set_chord_m(wing_chord_m)
super_cub_wing.set_center_of_gravity(wing_center_of_gravity)
# NACA WING parameters
super_cub_wing.set_NACA_from_data("2415", naca_data)

# TAIL
super_cub_tail = Tail()
super_cub_tail.set_span_m(tail_span_m)
super_cub_tail.set_chord_m(in_to_meters(tail_chord_in))
# NACA TAIL parameters
super_cub_tail.set_NACA_from_data("0009", naca_data)

# Additional tail parameters
super_cub_tail.set_tau(tau)
super_cub_tail.set_moment_arm_length_m(in_to_meters(wing_to_tail_dist_in))

# FUSELAGE
super_cub_fuselage = Fuselage()
super_cub_fuselage.set_length_m(fuselage_length_m)
super_cub_fuselage.set_height_m(fuselage_height_m)

# AIRCRAFT
super_cub = Aircraft("Super Cub", super_cub_wing, super_cub_tail, super_cub_fuselage)

def run_hw4_simulation():
    if DEBUG:
        print("\n")
        logging.info("----------------------------------------------------------------------------")
        logging.info(f"----------------------- HW 4 Aircraft: {super_cub._name} ---------------------------")
        logging.info("----------------------------------------------------------------------------")

        print_info_table(test_measurements, "TEST MEASUREMENTS INFORMATION")

    # Run simulation to get CL max, Cd0, and K
    uav_simulator_settings.set_plots(True) # Enable plots
    CL_max, Cd0, K = Simulate.run_aircraft_simulation(super_cub, test_measurements, wing_surface_area_m, tail_surface_area_m, wing_chord_m)

    # PROBLEM 3
    super_cub.set_trimmed_drag_polar_coefficients(Cd0, K)
    super_cub.set_weight(super_cub_weight_kg)
    super_cub.plot_thrust_and_power(test_measurements["Test Air Density (kg/m^3)"], test_measurements["Test Velocity Range (m/s)"])

    # TODO: Stall speed should be 9 or 8 m/s
    # TODO: get this from CL vs alpha (~1.4) if you assume higher, you'll just get something that flys slower 
        # CL max = stall