from util.uav_logger import *
from util.helpers import *
from src.aircraft import *
from src.setup import *

from collections import namedtuple

# Set DEBUG option
DEBUG = True

print("\n")
msg = "Welcome to UAV Sim!"
print(msg)
print("\n")

# test imports
logging.info('Logging enabled')
logging.info(f"Log level: {logging.getLogger().getEffectiveLevel()}")
print("\n")

# Test Values
alpha_deg_test_value = test_measurements["Test Alpha (degrees)"]
h_test_value = test_measurements["Test h"]
delta_e_deg_test_value = test_measurements["Test Delta_e (degrees)"]
Reynolds_test = test_measurements["Test Reynolds Number"]
i_h_test_value = test_measurements["Test i_h"]

# WING
super_cub_wing = Wing()
super_cub_wing.set_span(in_to_meters(wing_span_in))
super_cub_wing.set_chord(in_to_meters(wing_chord_in))
super_cub_wing.set_center_of_gravity(wing_center_of_gravity)
NACA_2415 = NACA("2415", Cd_2415, CL_2415, Cd0_2415, deg_to_rad(alpha_0_2415_deg), super_cub_wing.get_AR(), e_wing)
NACA_2415.set_CL_window(CL_2415_start, CL_2415_end)
NACA_2415.set_alpha_window(alpha_2415_start_deg, alpha_2415_end_deg) # NOTE: OK to use degrees here; converted to rad in a_2D calc
NACA_2415.set_CM_aero_center(CMac_wing_2415)
super_cub_wing.set_NACA(NACA_2415)

CL_wing = super_cub_wing.find_CL_NACA(deg_to_rad(alpha_deg_test_value))
CD_wing = super_cub_wing.find_CD_NACA()
CM_wing = super_cub_wing.find_CM(h_test_value)

if DEBUG:
    wing_info = {
        "Wing Span": super_cub_wing.get_span(),
        "Wing Chord": super_cub_wing.get_chord(),
        "Wing Center of Gravity": super_cub_wing.get_center_of_gravity(),
        "CL Wing": CL_wing,
        "CD Wing": CD_wing,
        "CM Wing": CM_wing
    }
    NACA_2415_info = NACA_2415.export_variables_to_dict()
    print_info_table(NACA_2415_info, "NACA 2415 INFORMATION")
    print_info_table(wing_info, "WING INFORMATION")

# TAIL
super_cub_tail = Tail()
super_cub_tail.set_span(in_to_meters(tail_span_in))
super_cub_tail.set_chord(in_to_meters(tail_chord_in))
NACA_0009 = NACA("0009", Cd_0009, CL_0009, Cd0_0009, deg_to_rad(alpha_0_0009_deg), super_cub_tail.get_AR(), e_tail)
NACA_0009.set_CL_window(CL_0009_start, CL_0009_end)
NACA_0009.set_alpha_window(alpha_0009_start_deg, alpha_0009_end_deg) # NOTE: OK to use degrees here; converted to rad in a_2D calc
super_cub_tail.set_NACA(NACA_0009)

# NOTE: OK to use CL wing and AR to calculate epsion
super_cub_tail.set_epsilon(super_cub_tail.find_epsilon(CL_wing, NACA_0009.get_e(), NACA_2415.get_AR()))
super_cub_tail.set_tau(tau)

CL_tail = super_cub_tail.find_CL(deg_to_rad(alpha_deg_test_value), deg_to_rad(delta_e_deg_test_value), i_h_test_value)
CD_tail = super_cub_tail.find_CD_NACA()

# Set moment arm so we can calcuate CM
super_cub_tail.set_moment_arm_length(in_to_meters(wing_to_tail_dist_in))
CM_tail = super_cub_tail.find_CM(in_to_meters(tail_surface_area_in), in_to_meters(wing_surface_area_in), in_to_meters(wing_chord_in), CL_tail)

if DEBUG:
    tail_info = {
        "Tail Span": super_cub_tail.get_span(),
        "Tail Chord": super_cub_tail.get_chord(),
        "Tail Epsilon": super_cub_tail.get_epsilon(),
        "Tail Tau": super_cub_tail.get_tau(),
        "CL Tail": CL_tail,
        "CD Tail": CD_tail,
        "CM Tail": CM_tail,
    }
    NACA_0009_info = NACA_0009.export_variables_to_dict()
    print_info_table(NACA_0009_info, "NACA 0009 INFORMATION")
    print_info_table(tail_info, "TAIL INFORMATION")

if DEBUG:
    print_info_table(test_measurements, "TEST MEASUREMENTS INFORMATION")

# FUSELAGE
super_cub_fuselage = Fuselage()
super_cub_fuselage.set_length(in_to_meters(fuselage_length_in))
super_cub_fuselage.set_height(in_to_meters(fuselage_height_in))

CD_fuselage = super_cub_fuselage.find_CD(Reynolds_test, in_to_meters(wing_chord_in))
# TODO: adjust super_cub_fuselage volume by * 1/3 for taper
volume_taper_percent = (1/3)
CM_fuselage = super_cub_fuselage.find_CM(deg_to_rad(alpha_deg_test_value), in_to_meters(wing_surface_area_in), in_to_meters(wing_chord_in), volume_taper_percent)

if DEBUG:
    fuselage_info = {
        "Fuselage Length": super_cub_fuselage.get_length(),
        "Fuselage Height": super_cub_fuselage.get_height(),
        "CD Fuselage": CD_fuselage,
        "CM Fuselage": CM_fuselage,
    }
    print_info_table(fuselage_info, "FUSELAGE INFORMATION")

# AIRCRAFT
super_cub = Aircraft("Super Cub", super_cub_wing, super_cub_tail, super_cub_fuselage)

super_cub.set_i_h(i_h_test_value)

super_cub.set_wing_surface_area_in(wing_surface_area_in)
    
super_cub.set_tail_surface_area_in(tail_surface_area_in)
    
super_cub.set_wing_chord_in(wing_chord_in)
    
super_cub.simulate(alpha_deg_test_value, delta_e_deg_test_value, Reynolds_test, h_test_value)

# TODO: Stall speed should be 9 or 8 m/s
# TODO: get this from CL vs alpha (~1.4) if you assume higher, you'll just get something that flys slower 
    # CL max = stall 