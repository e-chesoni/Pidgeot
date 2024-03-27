import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import minimize_scalar

from util.uav_logger import *
from src.settings import *
from src.setup import *
from src.simulate import *
from simulations.hw6.setup import *
from src.aerofoil import *
from src.aircraft import *
from src.wing import *
from src.tail import *
from src.fuselage import *


# Set DEBUG option
DEBUG = True

# WING
highway_pursuit_wing = Wing()
highway_pursuit_wing.set_span_m(wing_span_m)
highway_pursuit_wing.set_chord_m(wing_chord_m)
highway_pursuit_wing.set_center_of_gravity(wing_center_of_gravity)
# NACA WING parameters
#highway_pursuit_wing.set_NACA_from_data("4415", naca_data)

# NOTE: Testing adding a flap
# NOTE: top curve on 4415 graph shows data for flap with delta = 60deg
highway_pursuit_wing.set_NACA_from_data("4415_with_Flap", naca_data)

# TAIL
highway_pursuit_tail = Tail()
highway_pursuit_tail.set_span_m(tail_span_m)
highway_pursuit_tail.set_chord_m(tail_chord_m)
# NACA TAIL parameters
highway_pursuit_tail.set_NACA_from_data("0009", naca_data)

# Additional tail parameters
highway_pursuit_tail.set_tau(tau)
highway_pursuit_tail.set_moment_arm_length_m(wing_to_tail_dist_m)

# FUSELAGE
highway_pursuit_fuselage = Fuselage()
highway_pursuit_fuselage.set_length_m(fuselage_length_m)
highway_pursuit_fuselage.set_height_m(fuselage_height_m)

# Create aircraft
highway_pursuit = Aircraft("Highway Pursuit", highway_pursuit_wing, highway_pursuit_tail, highway_pursuit_fuselage)

def run_hw6_simulation():
    if DEBUG:
        print("\n")
        logging.info("----------------------------------------------------------------------------")
        logging.info(f"--------------------- HW 6 Aircraft: {highway_pursuit._name} -----------------------")
        logging.info("----------------------------------------------------------------------------")

        print_info_table(test_measurements, "TEST MEASUREMENTS INFORMATION")
    
    # Run simulation to get CL max, Cd0, and K
    uav_simulator_settings.set_plots(False)
    uav_simulator_settings.set_apply_stall_model(False)
    #uav_simulator_settings.set_delta_deflection_down(False) # we do this for the landing calcuation later; delta deflecting up slows the plane down
    CL_max, Cd0, K = Simulate.run_aircraft_simulation(highway_pursuit, test_measurements, wing_surface_area_m, tail_surface_area_m, wing_chord_m)

    # Run weight simulation
    # TODO: Package this as a simulation
    # Weight Calcuations
    highway_pursuit.set_W0(total_weight_kg)
    highway_pursuit.set_We_over_W0(We_over_W0)
    highway_pursuit.set_Wf_over_W0(highway_pursuit.find_Wf_over_W0(Range_km, H_F_km, L_over_D_cruise, eta_p))
    highway_pursuit.set_Wp(highway_pursuit.find_Wp())

    highway_pursuit.set_trimmed_drag_polar_coefficients(CD_trimmed, K_trimmed)
    highway_pursuit.set_wing_surface_area_m(highway_pursuit.find_wing_surface_area(test_measurements["Test Air Density (kg/m^3)"], V_m_per_s, CL_test)) # TODO: try flying at a lower CL
    hp_wing_length, hp_wing_width = highway_pursuit.calculate_wing_dimensions_m()

    # Run simulation to find landing speed
    # TODO: Package this as a simulation
    # NOTE: You also have calculated cl_max from simulation above
    CL_max_for_landing = (0.9) * CL_max # NOTE: Told to take 0.9 of CL_max in problem statement    

    #landing_lift, landing_drag, landing_deceleration = Simulate.simulate_landing(test_measurements, CL_max, Cd0, K, wing_surface_area_m, landing_velocity_ms)
    # NOTE: For + flap, use cl max = 2.8 (from graph)
    landing_lift, landing_drag, landing_velocity_ms, landing_deceleration = Simulate.simulate_landing(test_measurements, CL_max, Cd0, K, wing_surface_area_m, landing_runway_length_m)

    # Run simulation for tail sizing
    # TODO: Use tail volume equation

    if DEBUG:
        hp_weight_info = {
            "Total Weight (kg)": highway_pursuit.get_W0(),
            "Payload Weight (kg)": highway_pursuit.get_Wp(),
            "Wing Surface Area (meters)": highway_pursuit.get_wing_surface_area_m(),
            "Potential Wing Length (meters)": hp_wing_length,
            "Potential Wing Width (meters)": hp_wing_width,
        }
        print_info_table(hp_weight_info, "HIGHWAY PURSUIT WEIGHT-IN")

        hp_landing_info = {
            "CL Max": CL_max,
            "CL Max for Landing": CL_max_for_landing,
            "Landing Lift (N)": landing_lift,
            "Landing Drag (N)": landing_drag,
            "Landing Velocity (ms)": landing_velocity_ms,
            "Required Deceleration (m/s^2)": landing_deceleration
        }
        print_info_table(hp_landing_info, "HIGHWAY PURSUIT LANDING INFORMATION")



