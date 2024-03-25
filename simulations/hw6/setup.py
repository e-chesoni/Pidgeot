import numpy as np
import json
import os

from util.helpers import *
from src.NACA import *
from util.uav_logger import *
from util.helpers import *
from src.aircraft import *

# TODO: Remove Later
hw_round = 6

NACA_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'NACA.json'))
aircraft_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'aircrafts.json'))

# Load both JSON files
with open(NACA_file_path, 'r') as naca_file, open(aircraft_file_path, 'r') as aircraft_file:
    naca_data = json.load(naca_file)
    aircraft_data = json.load(aircraft_file)

# Extract wing parameters
wing_span_m = aircraft_data["highway_pursuit"]["wing"]["span_m"]
wing_chord_m = aircraft_data["highway_pursuit"]["wing"]["chord_m"]
wing_center_of_gravity = aircraft_data["highway_pursuit"]["wing"]["center_of_gravity"]
wing_surface_area_m = wing_span_m * wing_chord_m

# Extract tail parameters
tail_span_m = aircraft_data["highway_pursuit"]["tail"]["span_m"]
tail_chord_m = aircraft_data["highway_pursuit"]["tail"]["chord_m"]
elevator_chord_m = aircraft_data["highway_pursuit"]["tail"]["elevator_chord_m"]
tail_thickness_m = aircraft_data["highway_pursuit"]["tail"]["thickness_m"]
tail_surface_area_m = tail_span_m * tail_chord_m

# Test Measurements
# NOTE: Define test measurements in a dictionary
test_measurements = {
    "Test Alpha (degrees)": 30, # NOTE: for main impl: alpha range -30 to 30 (-0.524 - 0.524 in rads) intervals of 5
    "Test Alpha Range (degrees)": np.linspace(-10, 30, 21),
    "Test Delta_e (degrees)": 20,
    "Test Delta_e List (degrees)": [0, 5, 10],
    "Test Reynolds Number": 6e5,
    "Test h": 0.25,
    "Test i_h (meters)": 0,
    "Test Critical Angle of Attack (degrees)": 12,
    "Test Velocity Range (m/s)": np.linspace(0, 30, 100),
    "Test Air Density (kg/m^3)": 1.225,
}

# Fuselage parameters
fuselage_length_m = (1/3) * wing_span_m # NOTE: Same as super cub (eyeballed)
fuselage_height_m = (4/5) * wing_chord_m # NOTE: Same as super cub (eyeballed)

tau = 0.7

# Combined Parameters
wing_to_tail_dist_m = 0.4572

# Weight Setup
Range_km = 30
H_F_km = 50
L_over_D_cruise = 5 # TODO: try changing for better results
eta_p = 0.4

total_weight_kg = 7.5
We_over_W0 = 0.5 # NOTE: From empirical data

CD_trimmed = 0.03
K_trimmed = 0.08

CL_max = CD_trimmed / K_trimmed
CL_test = 0.2

V_m_per_s = 45 # NOTE: Requirement is 100mph ~ 44.7 m/s