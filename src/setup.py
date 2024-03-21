import numpy as np

from util.helpers import *
from src.NACA import *
from util.uav_logger import *
from util.helpers import *
from src.aircraft import *

# NOTE: Do not put conversions in setup
# Super Cub Parameters
super_cub_weight_kg = 750

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
    "Test Alpha Range (degrees)": np.linspace(-10, 30, 21),
    "Test Delta_e (degrees)": 20,
    "Test Delta_e List (degrees)": [0, 5, 10],
    "Test Reynolds Number": 6e5,
    "Test h": 0.25,
    "Test i_h": 0,
    "Test Critical Angle of Attack (degrees)": 12,
    "Test Velocity Range (m/s)": np.linspace(0, 30, 100),
    "Test Air Density (kg/m^3)": 1.225,
}

dataset_1 = {
    "J": [0.406, 0.433, 0.457, 0.477, 0.500, 0.522, 0.544, 0.567, 0.593, 0.616, 0.641, 0.668, 0.689, 0.715, 0.737, 0.764, 0.783, 0.806, 0.829, 0.858, 0.882, 0.906, 0.929],
    "CT": [0.0955, 0.0922, 0.0890, 0.0862, 0.0828, 0.0790, 0.0759, 0.0721, 0.0672, 0.0633, 0.0585, 0.0530, 0.0486, 0.0423, 0.0379, 0.0313, 0.0273, 0.0222, 0.0168, 0.0094, 0.0035, -0.0023, -0.0077],
    "CP": [0.0619, 0.0616, 0.0612, 0.0606, 0.0599, 0.0586, 0.0577, 0.0563, 0.0543, 0.0525, 0.0503, 0.0474, 0.0449, 0.0413, 0.0385, 0.0344, 0.0318, 0.0286, 0.0251, 0.0198, 0.0153, 0.0107, 0.0060],
    "eta": [0.627, 0.648, 0.665, 0.678, 0.691, 0.703, 0.715, 0.726, 0.734, 0.742, 0.746, 0.747, 0.746, 0.733, 0.724, 0.696, 0.671, 0.625, 0.555, 0.409, 0.201, -0.192, -1.178]
}

dataset_2 = {
    "J": [0.096, 0.121, 0.143, 0.167, 0.191, 0.217, 0.241, 0.266, 0.291, 0.311, 0.339, 0.362, 0.383, 0.406, 0.429, 0.453, 0.476],
    "CT": [0.1195, 0.1190, 0.1180, 0.1171, 0.1162, 0.1150, 0.1132, 0.1111, 0.1093, 0.1068, 0.1042, 0.1015, 0.0988, 0.0961, 0.0929, 0.0897, 0.0863],
    "CP": [0.0583, 0.0590, 0.0595, 0.0601, 0.0607, 0.0614, 0.0617, 0.0621, 0.0625, 0.0624, 0.0626, 0.0626, 0.0623, 0.0622, 0.0618, 0.0613, 0.0607],
    "eta": [0.197, 0.244, 0.284, 0.326, 0.365, 0.407, 0.442, 0.476, 0.508, 0.533, 0.564, 0.587, 0.607, 0.627, 0.645, 0.662, 0.678]
}