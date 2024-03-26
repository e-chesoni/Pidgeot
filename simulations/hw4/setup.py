import numpy as np
import json
import os

from util.helpers import *
from src.NACA import *
from util.uav_logger import *
from util.helpers import *
from src.aircraft import *

NACA_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'NACA.json'))
aircraft_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'aircrafts.json'))

# Load both JSON files
with open(NACA_file_path, 'r') as naca_file, open(aircraft_file_path, 'r') as aircraft_file:
    naca_data = json.load(naca_file)
    aircraft_data = json.load(aircraft_file)

# NOTE: Do not put conversions in setup
# Super Cub Parameters
super_cub_weight_kg = aircraft_data["super_cub"]["weight_kg"]

# Wing parameters
wing_span_in = aircraft_data["super_cub"]["wing"]["span_in"]
wing_span_m = in_to_meters(wing_span_in)
wing_chord_in = aircraft_data["super_cub"]["wing"]["chord_in"]
wing_chord_m = in_to_meters(wing_chord_in)
wing_center_of_gravity = aircraft_data["super_cub"]["wing"]["center_of_gravity"] # percent distance from wing tip
# NOTE: Simplified surface area is the product of the span and the chord
wing_surface_area_in = wing_span_in * wing_chord_in
wing_surface_area_m = in_to_meters(wing_surface_area_in)

# Tail parameters
tail_span_in = aircraft_data["super_cub"]["tail"]["span_in"]
tail_span_m = in_to_meters(tail_span_in)
tail_chord_in = aircraft_data["super_cub"]["tail"]["chord_in"]
tail_chord_m = in_to_meters(tail_chord_in)
elevator_chord_in = aircraft_data["super_cub"]["tail"]["elevator_chord_in"]
elevator_chord_m = in_to_meters(elevator_chord_in)
tail_thickness_in = aircraft_data["super_cub"]["tail"]["thickness_in"]
tail_thickness_m = in_to_meters(tail_thickness_in)
tail_surface_area_in = tail_span_in * tail_chord_in
tail_surface_area_m = in_to_meters(tail_surface_area_in)

# Fuselage parameters
fuselage_length_in = (1/3) * wing_span_in # NOTE: Looks like ~1/3 wing span
fuselage_length_m = in_to_meters(fuselage_length_in)
fuselage_height_in = (4/5) * wing_chord_in # NOTE: Looks like ~4/5 wing chord
fuselage_height_m = in_to_meters(fuselage_height_in)

tau = 0.7

# Combined Parameters
wing_to_tail_dist_in = 18
wing_to_tail_dist_m = in_to_meters(wing_to_tail_dist_in)

# NACA 2415 Parameters (for Wing)
CMac_wing_2415 = 0.18
h_cg_wing = 0.4 # cg of the wing
eta_tail_super = 0.5