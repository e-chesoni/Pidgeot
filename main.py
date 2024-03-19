import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.optimize import curve_fit

from util.uav_logger import *
from util.helpers import *
from src.aircraft import *
from src.setup import *

# Set DEBUG option
DEBUG = True

print("\n")
msg = "Welcome to UAV Sim!"
print(msg)
print("\n")

# TODO: Test imports
logging.info('Logging enabled')
logging.info(f"Log level: {logging.getLogger().getEffectiveLevel()}")
print("\n")

# Test Values
alpha_deg_test_value = test_measurements["Test Alpha (degrees)"]
alpha_range_deg_test_value = test_measurements["Test Alpha Range (degrees)"]
delta_e_deg_test_value = test_measurements["Test Delta_e (degrees)"]
delta_e_list_deg_test_value = test_measurements["Test Delta_e List (degrees)"]
Reynolds_test_value = test_measurements["Test Reynolds Number"]
i_h_test_value = test_measurements["Test i_h"]
h_test_value = test_measurements["Test h"]

# PROBLEM 1
# WING
super_cub_wing = Wing()
super_cub_wing.set_span(in_to_meters(wing_span_in))
super_cub_wing.set_chord(in_to_meters(wing_chord_in))
super_cub_wing.set_center_of_gravity(wing_center_of_gravity)
NACA_2415 = NACA("2415", Cd_2415, CL_2415, Cd0_2415, deg_to_rad(alpha_0_2415_deg), super_cub_wing.get_AR(), e_wing)
NACA_2415.set_CL_window(CL_2415_start, CL_2415_end)
NACA_2415.set_alpha_window(alpha_2415_start_deg, alpha_2415_end_deg) # NOTE: OK to use degrees here; converted to rad in a_2D calc
NACA_2415.set_CM_aero_center(CMac_wing_2415)
super_cub_wing.set_NACA(NACA_2415)

# TAIL
super_cub_tail = Tail()
super_cub_tail.set_span(in_to_meters(tail_span_in))
super_cub_tail.set_chord(in_to_meters(tail_chord_in))
NACA_0009 = NACA("0009", Cd_0009, CL_0009, Cd0_0009, deg_to_rad(alpha_0_0009_deg), super_cub_tail.get_AR(), e_tail)
NACA_0009.set_CL_window(CL_0009_start, CL_0009_end)
NACA_0009.set_alpha_window(alpha_0009_start_deg, alpha_0009_end_deg) # NOTE: OK to use degrees here; converted to rad in a_2D calc
super_cub_tail.set_NACA(NACA_0009)
super_cub_tail.set_tau(tau)
super_cub_tail.set_moment_arm_length(in_to_meters(wing_to_tail_dist_in))

# FUSELAGE
super_cub_fuselage = Fuselage()
super_cub_fuselage.set_length(in_to_meters(fuselage_length_in))
super_cub_fuselage.set_height(in_to_meters(fuselage_height_in))

if DEBUG:
    print_info_table(test_measurements, "TEST MEASUREMENTS INFORMATION")

# AIRCRAFT
super_cub = Aircraft("Super Cub", super_cub_wing, super_cub_tail, super_cub_fuselage)

# Enable debugging on aircraft
super_cub.set_log_level(1)

# Set variables on aircraft for testing
super_cub.set_i_h(i_h_test_value)
super_cub.set_wing_surface_area_in(wing_surface_area_in)
super_cub.set_tail_surface_area_in(tail_surface_area_in)
super_cub.set_wing_chord_in(wing_chord_in)

# Run simulation
super_cub.simulate(alpha_deg_test_value, delta_e_deg_test_value, Reynolds_test_value, h_test_value)

# Call plotting function
super_cub.plot_aero_curves(alpha_range_deg_test_value, delta_e_list_deg_test_value, Reynolds_test_value, h_test_value)

# PROBLEM 2
# Find trimmed elevator angle for a range of angles of attack
trimmed_data = []

# NOTE: Print statements causes lambda function to fail; need to turn them off for P2
super_cub.set_log_level(3)

for alpha_deg in alpha_range_deg_test_value:
    f_CM = lambda del_e_deg: super_cub.simulate(alpha_deg, del_e_deg, Reynolds_test_value, h_test_value)[-1]  # Access CM directly
    print(f_CM)
    del_e_deg_trim = fsolve(f_CM, 0)[0]
    # Now unpack the returned values in the order of CL, CD, CM
    result = super_cub.simulate(alpha_deg, del_e_deg_trim, Reynolds_test_value, h_test_value)
    CL, CD, CM = result.CL, result.CD, result.CM
    trimmed_data.append((CM, CL, CD))

# Extract CL and CD for curve fitting
CL_data = [data[1] for data in trimmed_data]
CD_data = [data[2] for data in trimmed_data]

# Fit the parabolic drag polar equation
def drag_polar(CL, Cd0, K):
    return Cd0 + K * CL**2

popt, pcov = curve_fit(drag_polar, CL_data, CD_data)
Cd0, K = popt

print(f"Cd0: {Cd0}, K: {K}")

# TODO: Stall speed should be 9 or 8 m/s
# TODO: get this from CL vs alpha (~1.4) if you assume higher, you'll just get something that flys slower 
    # CL max = stall 