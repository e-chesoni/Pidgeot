import numpy as np
import pandas as pd
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
propeller_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'propellers.json'))
motor_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'motors.json'))


# Load both JSON files
with open(NACA_file_path, 'r') as naca_file, \
     open(aircraft_file_path, 'r') as aircraft_file, \
     open(propeller_file_path, 'r') as propeller_file, \
     open(motor_file_path, 'r') as motor_file:
    naca_data = json.load(naca_file)
    aircraft_data = json.load(aircraft_file)
    propeller_data = json.load(propeller_file)
    motor_data = json.load(motor_file)


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

CD_trimmed = 0.028
K_trimmed = 0.069

#CL_max_no_flap = math.sqrt(CD_trimmed / K_trimmed)
CL_test = 0.2

V_m_per_s = 45 # NOTE: Requirement is 100mph ~ 44.7 m/s

# Landing Setup
landing_runway_length_m = ft_to_meters(200)

# Propeller setup
# Extracting data for PKZ1005
propeller_data = propeller_data['PKZ1005']

# Creating a DataFrame
propeller_df = pd.DataFrame(propeller_data)

# Motor setup
test_motor = motor_data["480-DC-Motor"]
