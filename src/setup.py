from util.helpers import *
from src.NACA import *
from util.uav_logger import *
from util.helpers import *
from src.aircraft import *

# NOTE: Do not put conversions in setup

# Wing parameters
wing_span_in = 47
wing_chord_in = 7.5
wing_center_of_gravity = 0.4 # percent distance from wing tip
# NOTE: Simplified surface area is the product of the span and the chord
wing_surface_area_in = wing_span_in * wing_chord_in

# Tail parameters
tail_span_in = 16
tail_chord_in = 5
elevator_chord_in = 2
tail_thickness_in = 0.25
tail_surface_area_in = tail_span_in * tail_chord_in

# Fuselage parameters
fuselage_length_in = (1/3) * wing_span_in # NOTE: Looks like ~1/3 wing span
fuselage_height_in = (4/5) * wing_chord_in # NOTE: Looks like ~4/5 wing chord

tau = 0.7

# Combined Parameters
wing_to_tail_dist_in = 18

# NACA 2415 Parameters (for Wing)
CMac_wing_2415 = 0.18
h_cg_wing = 0.4 # cg of the wing
eta_tail_super = 0.5

Cd_2415 = 0.017
Cd0_2415 = 0.01
CL_2415 = 1

alpha_0_2415_deg = -2

CL_2415_start = 0.2
CL_2415_end = 0.6

# NOTE: We do not need to convert to radian here becasue conversion occurs when we calculate a_2D
alpha_2415_start_deg = 0
alpha_2415_end_deg = 4
e_wing = 0.7 # WAG

# NACA 0009 Parameters (for tail)
Cd_0009 = 0.014
Cd0_0009 = 0.009
CL_0009 = 0.6
alpha_0_0009_deg = -10

CL_0009_start = 1.2
CL_0009_end = 1.6

# NOTE: We do not need to convert to radian here becasue conversion occurs when we calculate a_2D
alpha_0009_start_deg = 0
alpha_0009_end_deg = 4
e_tail = 0.6 # WAG

# Test Measurements
# NOTE: Define test measurements in a dictionary
test_measurements = {
    "Test Alpha (degrees)": 30, # NOTE: for main impl: alpha range -30 to 30 (-0.524 - 0.524 in rads) intervals of 5
    "Test h": 0.25,
    "Test Delta_e (degrees)": 20,
    "Test i_h": 0,
    "Test Reynolds Number": 2 * (10**5)
}
