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

DEBUG = True

highway_pursuit_wing = Wing()
highway_pursuit_tail = Tail()
highway_pursuit_fuselage = Fuselage()
highway_pursuit = Aircraft("Highway Pursuit", highway_pursuit_wing, highway_pursuit_tail, highway_pursuit_fuselage)

highway_pursuit.set_W0(total_weight_kg)
highway_pursuit.set_We_over_W0(We_over_W0)
highway_pursuit.set_Wf_over_W0(highway_pursuit.find_Wf_over_W0(Range_km, H_F_km, L_over_D_cruise, eta_p))
highway_pursuit.set_Wp(highway_pursuit.find_Wp())

highway_pursuit.set_trimmed_drag_polar_coefficients(CD_trimmed, K_trimmed)
highway_pursuit.set_wing_surface_area_m(highway_pursuit.find_wing_surface_area(rho_sea_level, V_m_per_s, CL_test)) # TODO: try flying at a lower CL
hp_wing_length, hp_wing_width = highway_pursuit.calculate_wing_dimensions_m()

def run_hw6_simulation():
    logging.info(f"Running HW{hw_round} Simulation...\n")

    if DEBUG:
        hp_info = {
            "Total Weight W0": highway_pursuit.get_W0(),
            "Payload Weight": highway_pursuit.get_Wp(),
            "Wing Surface Area (meters)": highway_pursuit.get_wing_surface_area_m(),
            "Potential Wing Length (meters)": hp_wing_length,
            "Potential Wing Width (meters)": hp_wing_width,
        }
        print_info_table(hp_info, "HIGHWAY PURSUIT UAV INFORMATION")
