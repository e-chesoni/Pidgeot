import numpy as np
import json
import os

from util.helpers import *
from src.NACA import *
from util.uav_logger import *
from util.helpers import *
from src.aircraft import *

NACA_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'NACA.json'))

# Load the JSON file
with open(NACA_file_path, 'r') as file:
    naca_data = json.load(file)

# Load the JSON file
aircraft_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'aircrafts.json'))

with open(aircraft_file_path, 'r') as file:
    aircraft_data = json.load(file)

# Extract parameters for Super Cub
super_cub_weight_kg = aircraft_data["super_cub"]["weight_kg"]

# Wing parameters
wing_span_in = aircraft_data["super_cub"]["wing"]["span_in"]
wing_chord_in = aircraft_data["super_cub"]["wing"]["chord_in"]
wing_center_of_gravity = aircraft_data["super_cub"]["wing"]["center_of_gravity"]
wing_surface_area_in = wing_span_in * wing_chord_in

# Tail parameters
tail_span_in = aircraft_data["super_cub"]["tail"]["span_in"]
tail_chord_in = aircraft_data["super_cub"]["tail"]["chord_in"]
elevator_chord_in = aircraft_data["super_cub"]["tail"]["elevator_chord_in"]
tail_thickness_in = aircraft_data["super_cub"]["tail"]["thickness_in"]
tail_surface_area_in = tail_span_in * tail_chord_in

# Fuselage parameters
fuselage_length_in = (1/3) * wing_span_in
fuselage_height_in = (4/5) * wing_chord_in

tau = 0.7

# Combined Parameters
wing_to_tail_dist_in = 18

# Accessing NACA 2415 parameters
Cd_2415 = naca_data["NACA_2415"]["Cd"]
Cd0_2415 = naca_data["NACA_2415"]["Cd0"]
CL_2415 = naca_data["NACA_2415"]["CL"]
alpha_0_2415_deg = naca_data["NACA_2415"]["alpha_0_deg"]
CL_2415_start = naca_data["NACA_2415"]["CL_start"]
CL_2415_end = naca_data["NACA_2415"]["CL_end"]
# Do not need to convert to rad here; done later
alpha_2415_start_deg = naca_data["NACA_2415"]["alpha_start_deg"]
alpha_2415_end_deg = naca_data["NACA_2415"]["alpha_end_deg"]
e_wing = naca_data["NACA_2415"]["e"]

# Accessing NACA 0009 parameters
Cd_0009 = naca_data["NACA_0009"]["Cd"]
Cd0_0009 = naca_data["NACA_0009"]["Cd0"]
CL_0009 = naca_data["NACA_0009"]["CL"]
alpha_0_0009_deg = naca_data["NACA_0009"]["alpha_0_deg"]
CL_0009_start = naca_data["NACA_0009"]["CL_start"]
CL_0009_end = naca_data["NACA_0009"]["CL_end"]
# Do not need to convert to rad here; done later
alpha_0009_start_deg = naca_data["NACA_2415"]["alpha_start_deg"]
alpha_0009_end_deg = naca_data["NACA_2415"]["alpha_end_deg"]
e_tail = naca_data["NACA_2415"]["e"]

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