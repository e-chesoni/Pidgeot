import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.optimize import curve_fit

from util.uav_logger import *
from util.helpers import *
from src.main_setup import *
from src.aircraft import *
from simulations.hw4.setup import *

# Set DEBUG option
DEBUG = True

# Test Values
alpha_deg_test_value = test_measurements["Test Alpha (degrees)"]
alpha_range_deg_test_value = test_measurements["Test Alpha Range (degrees)"]
delta_e_deg_test_value = test_measurements["Test Delta_e (degrees)"]
delta_e_list_deg_test_value = test_measurements["Test Delta_e List (degrees)"]
Reynolds_test_value = test_measurements["Test Reynolds Number"]
i_h_m_test_value = test_measurements["Test i_h (meters)"]
h_test_value = test_measurements["Test h"]
critical_angle_of_attack_test_value = test_measurements["Test Critical Angle of Attack (degrees)"]
velocity_range_ms_test_value = test_measurements["Test Velocity Range (m/s)"]
rho_test_value = test_measurements["Test Air Density (kg/m^3)"]

# PROBLEM 1
# WING
super_cub_wing = Wing()
super_cub_wing.set_span(in_to_meters(wing_span_in))
super_cub_wing.set_chord(in_to_meters(wing_chord_in))
super_cub_wing.set_center_of_gravity(wing_center_of_gravity)

# NACA WING parameters
super_cub_wing.set_NACA_from_data("2415", naca_data)

# TAIL
super_cub_tail = Tail()
super_cub_tail.set_span(in_to_meters(tail_span_in))
super_cub_tail.set_chord(in_to_meters(tail_chord_in))

super_cub_wing.set_NACA_from_data("0009", naca_data)
NACA_0009 = NACA("0009", Cd_0009, CL_0009, Cd0_0009, deg_to_rad(alpha_0_0009_deg), super_cub_tail.get_AR(), e_tail)
NACA_0009.set_CL_window(CL_0009_start, CL_0009_end)
NACA_0009.set_alpha_window(alpha_0009_start_deg, alpha_0009_end_deg) # NOTE: OK to use degrees here; converted to rad in a_2D calc
super_cub_tail.set_NACA(NACA_0009)

# Additional tail parameters
super_cub_tail.set_tau(tau)
super_cub_tail.set_moment_arm_length(in_to_meters(wing_to_tail_dist_in))

# FUSELAGE
super_cub_fuselage = Fuselage()
super_cub_fuselage.set_length(in_to_meters(fuselage_length_in))
super_cub_fuselage.set_height(in_to_meters(fuselage_height_in))

def run_hw4_simulation():
    if DEBUG:
        print_info_table(test_measurements, "TEST MEASUREMENTS INFORMATION")

    # AIRCRAFT
    super_cub = Aircraft("Super Cub", super_cub_wing, super_cub_tail, super_cub_fuselage, Units.INCHES)

    # Enable debugging on aircraft
    super_cub.set_log_level(1)

    # Set variables on aircraft for testing
    super_cub.set_i_h(i_h_m_test_value)
    super_cub.set_wing_surface_area_in(wing_surface_area_in) # NOTE: also convers in to m and sets wing_surface_area_m on aircraft
    super_cub.set_tail_surface_area_in(tail_surface_area_in) # NOTE: also convers in to m and sets wing_surface_area_m on aircraft
    super_cub.set_wing_chord_in(wing_chord_in) # NOTE: also convers in to m and sets wing_surface_area_m on aircraft
    super_cub.set_critical_angle_of_attack(critical_angle_of_attack_test_value)

    # Run simulation
    super_cub.simulate(alpha_deg_test_value, delta_e_deg_test_value, Reynolds_test_value, h_test_value)

    # Call plotting function
    cl_max_list = super_cub.plot_aero_curves(alpha_range_deg_test_value, delta_e_list_deg_test_value, Reynolds_test_value, h_test_value)
    logging.info(f"CL_max: {cl_max_list[0]}")

    # PROBLEM 2
    # Find trimmed elevator angle for a range of angles of attack
    # NOTE: Print statements causes lambda function to fail; need to turn them off for P2
    super_cub.set_log_level(3)

    Cd0, K = super_cub.find_trimmed_drag_polar_coefficients(alpha_range_deg_test_value, Reynolds_test_value, h_test_value)
    logging.info(f"Cd0: {Cd0}, K: {K}")

    # PROBLEM 3
    super_cub.set_trimmed_drag_polar_coefficients(Cd0, K)
    super_cub.set_weight(kg_to_g(super_cub_weight_kg))
    super_cub.plot_thrust_and_power(rho_test_value, velocity_range_ms_test_value)
    logging.info(f"CL_max: {cl_max_list[0]}")

    # TODO: Stall speed should be 9 or 8 m/s
    # TODO: get this from CL vs alpha (~1.4) if you assume higher, you'll just get something that flys slower 
        # CL max = stall