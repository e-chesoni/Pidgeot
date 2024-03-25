import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import minimize_scalar

from util.uav_logger import *
from simulations.hw6.setup import *
from src.aerofoil import *
from src.aircraft import *
from src.wing import *
from src.tail import *
from src.fuselage import *

# Set DEBUG option
DEBUG = True

# TODO: Move this to aircraft?
# Function to set wing paramerters


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

# WING
highway_pursuit_wing = Wing()
highway_pursuit_wing.set_span(wing_span_m)
highway_pursuit_wing.set_chord(wing_chord_m)
highway_pursuit_wing.set_center_of_gravity(wing_center_of_gravity)

# NACA WING parameters
highway_pursuit_wing.set_NACA_from_data("4415", naca_data)

# TAIL
highway_pursuit_tail = Tail()
highway_pursuit_tail.set_span(tail_span_m)
highway_pursuit_tail.set_chord(tail_chord_m)

# NACA TAIL parameters
highway_pursuit_tail.set_NACA_from_data("0009", naca_data)

# Additional tail parameters
highway_pursuit_tail.set_tau(tau)
highway_pursuit_tail.set_moment_arm_length(in_to_meters(wing_to_tail_dist_m))

highway_pursuit_fuselage = Fuselage()
highway_pursuit_fuselage.set_length(in_to_meters(fuselage_length_m))
highway_pursuit_fuselage.set_height(in_to_meters(fuselage_height_m))

highway_pursuit = Aircraft("Highway Pursuit", highway_pursuit_wing, highway_pursuit_tail, highway_pursuit_fuselage, Units.METERS)

# Enable debugging on aircraft
highway_pursuit.set_log_level(1)

# Set variables on aircraft for testing
highway_pursuit.set_i_h(i_h_m_test_value)
highway_pursuit.set_wing_surface_area_m(wing_surface_area_m) # NOTE: also convers in to m and sets wing_surface_area_m on aircraft
highway_pursuit.set_tail_surface_area_m(tail_surface_area_m) # NOTE: also convers in to m and sets wing_surface_area_m on aircraft
highway_pursuit.set_wing_chord_m(wing_chord_m) # NOTE: also convers in to m and sets wing_surface_area_m on aircraft
highway_pursuit.set_critical_angle_of_attack(critical_angle_of_attack_test_value)

# Run simulation
highway_pursuit.simulate(alpha_deg_test_value, delta_e_deg_test_value, Reynolds_test_value, h_test_value)

# Call plotting function
cl_max_list = highway_pursuit.plot_aero_curves(alpha_range_deg_test_value, delta_e_list_deg_test_value, Reynolds_test_value, h_test_value)

# Find Cd0 and K
highway_pursuit.set_log_level(3)

Cd0, K = highway_pursuit.find_trimmed_drag_polar_coefficients(alpha_range_deg_test_value, Reynolds_test_value, h_test_value)

# Weight Calcuations
highway_pursuit.set_W0(total_weight_kg)
highway_pursuit.set_We_over_W0(We_over_W0)
highway_pursuit.set_Wf_over_W0(highway_pursuit.find_Wf_over_W0(Range_km, H_F_km, L_over_D_cruise, eta_p))
highway_pursuit.set_Wp(highway_pursuit.find_Wp())

highway_pursuit.set_trimmed_drag_polar_coefficients(CD_trimmed, K_trimmed)
highway_pursuit.set_wing_surface_area_m(highway_pursuit.find_wing_surface_area(rho_test_value, V_m_per_s, CL_test)) # TODO: try flying at a lower CL
hp_wing_length, hp_wing_width = highway_pursuit.calculate_wing_dimensions_m()

def run_hw6_simulation():
    if DEBUG:
        logging.info(f"Running HW{hw_round} Simulation...\n")

        print_info_table(test_measurements, "TEST MEASUREMENTS INFORMATION")

        hp_info = {
            "Total Weight (kg)": highway_pursuit.get_W0(),
            "Payload Weight (kg)": highway_pursuit.get_Wp(),
            "Wing Surface Area (meters)": highway_pursuit.get_wing_surface_area_m(),
            "Potential Wing Length (meters)": hp_wing_length,
            "Potential Wing Width (meters)": hp_wing_width,
        }
        print_info_table(hp_info, "HIGHWAY PURSUIT UAV INFORMATION")

        logging.info(f"CL_max: {cl_max_list[0]}")
        logging.info(f"Cd0: {Cd0}, K: {K}")


