import math

import logging
from util.helpers import *
from src.settings import *


class Simulate():
    @staticmethod
     # NOTE: pass test measurements so we can hot-swap measurements
    def run_aircraft_simulation(aircraft, test_measurements, wing_surface_area_m, tail_surface_area_m, wing_chord_m):
        # Set log level
        aircraft.set_log_level(1)

        # Set variables on aircraft for testing
        aircraft.set_i_h(test_measurements["Test i_h (meters)"])
        aircraft.set_wing_surface_area_m(wing_surface_area_m)  # NOTE: also converts in to m and sets wing_surface_area_m on aircraft
        aircraft.set_tail_surface_area_m(tail_surface_area_m)  # NOTE: also converts in to m and sets wing_surface_area_m on aircraft
        aircraft.set_wing_chord_m(wing_chord_m)  # NOTE: also converts in to m and sets wing_surface_area_m on aircraft
        aircraft.set_critical_angle_of_attack(test_measurements["Test Critical Angle of Attack (degrees)"])

        # Run simulation
        CL, CD, CM = aircraft.simulate(test_measurements["Test Alpha (degrees)"], test_measurements["Test Delta_e (degrees)"],
                        test_measurements["Test Reynolds Number"], test_measurements["Test h"])
        
        # Print aircraft info
        aircraft.print_aircraft_info()
        
        logging.info(f"Total CL: {CL}")
        logging.info(f"Total CD: {CD}")
        logging.info(f"Total CM: {CM}")
        print("\n")

        # Find trimmed elevator angle for a range of angles of attack
        # NOTE: Print statements causes lambda function to fail; need to turn them off for P2
        aircraft.set_log_level(3)

        Cd0, K = aircraft.find_trimmed_drag_polar_coefficients(test_measurements["Test Alpha Range (degrees)"],
                                                            test_measurements["Test Reynolds Number"],
                                                            test_measurements["Test h"])

        if uav_simulator_settings.get_plot_setting():
            logging.info(f"Using plots to find CL_max")
            # Call plotting function
            cl_max_delta_e_dict = aircraft.plot_aero_curves(test_measurements["Test Alpha Range (degrees)"],
                                                    test_measurements["Test Delta_e List (degrees)"],
                                                    test_measurements["Test Reynolds Number"], test_measurements["Test h"])
            
            for c, d in cl_max_delta_e_dict.items():
                logging.info(f"CL_max: {c}, Delta_e_deg: {d}")
            
            CL_max, delta_e_deg = Simulate.find_cl_max_delta_e(cl_max_delta_e_dict)
        
        else:
            CL_max = aircraft.find_cl_max(Cd0, K)

        logging.info(f"Cd0: {Cd0}, K: {K}")
        print("\n")
        
        logging.info(f"CL_max used: {CL_max}")
        print("\n")

        return CL_max, Cd0, K
    
    def find_cl_max_delta_e(cl_max_delta_e_dict):
        # Get the max cl value and corresponding delta degree
        max_CL_max = -float('inf')  # Initialize to negative infinity to ensure any calculated CL_max will be greater
        max_delta_e_deg = None  # Initialize to None

        # Iterate over the dictionary items
        for CL_max, delta_e_deg in cl_max_delta_e_dict.items():
            # Check if the current CL_max is greater than the maximum CL_max found so far
            if CL_max > max_CL_max:
                # If yes, update the maximum CL_max and corresponding delta_e_deg
                max_CL_max = CL_max
                max_delta_e_deg = delta_e_deg

        return max_CL_max, max_delta_e_deg
    
    def find_cl_min_delta_e(cl_max_delta_e_dict):
        # Get the max cl value and corresponding delta degree
        min_CL_max = float('inf')  # Initialize to negative infinity to ensure any calculated CL_max will be greater
        min_delta_e_deg = None  # Initialize to None

        # Iterate over the dictionary items
        for CL_max, delta_e_deg in cl_max_delta_e_dict.items():
            # Check if the current CL_max is less than the maximum CL_max found so far
            logging.info(f"itr: cl max: {CL_max}")
            if CL_max < min_CL_max:
                # If yes, update the min CL_max and corresponding delta_e_deg
                logging.info(f"Updating current cl max {min_CL_max} to new min value: {CL_max}")
                min_CL_max = CL_max
                min_delta_e_deg = delta_e_deg

        return min_CL_max, min_delta_e_deg

    def simulate_landing(test_measurements, CL_max, Cd0, weight, wing_surface_area_m, runway_length):
        CL_max_for_landing = 0.9 * CL_max

        # Find landing velocity
        landing_velocity_ms = math.sqrt((2 * weight * test_measurements["Force of Gravity (m/s^2)"])/(CL_max * test_measurements["Test Air Density (kg/m^3)"] * wing_surface_area_m))

        # Find landing lift
        landing_lift = (CL_max_for_landing * test_measurements["Test Air Density (kg/m^3)"] * (landing_velocity_ms**2) * wing_surface_area_m) / 2

        # Find landing drag
        const = 0.5 * test_measurements["Test Air Density (kg/m^3)"] * (landing_velocity_ms**2) * wing_surface_area_m
        landing_drag = Cd0 * const

        # Find landing deceleartion
        landing_deceleration = (landing_velocity_ms**2) / (2*runway_length)

        return landing_lift, landing_drag, landing_velocity_ms, landing_deceleration

    # TODO: Is this true?
    # CG is influenced by wing_to_tail_dist_m; this is the distance from wing CG to tail CG
    def simulate_tail_sizing(tail_span_m, tail_chord_m, tail_surface_area_m, wing_to_tail_dist_m):
        V_tail_horizontal = None
        V_tail_vertical = None
        
        V_denom = tail_chord_m * tail_surface_area_m

        V_tail_horizontal = ( wing_to_tail_dist_m * tail_span_m ) / ( V_denom )
        l_v = 0.1
        S_v = 0.2
        V_tail_vertical = ( l_v * S_v ) / ( V_denom )

        return V_tail_horizontal, V_tail_vertical
    
    def simulate_required_RPM(aircraft, test_measurements, test_motor, V_m_per_s):
        # Find required thrust at cruise
        Tr_cruise, Pr_cruise = aircraft.find_thrust_power(V_m_per_s, test_measurements["Test Air Density (kg/m^3)"])

        # TODO: Find i_curr (motor current current)
        # For now, assume cruising current (i) of 2 amperes
        i_curr = 2  # in amperes
        Qm = aircraft.get_motor().calculate_Q(i_curr) # Q is the torque on the motor shaft from the coil
        omega = aircraft.get_motor().calculate_omega(Pr_cruise, Qm)
        required_rpm = rads_to_rpm(omega) # NOTE: The required RPM is way too high!
        required_battery_power = Qm * required_rpm
        required_voltage = required_battery_power / test_motor["i_0"] # volts
        '''
        NOTE: The current drawn can appear relatively low because the power (watts) is the product of voltage and current (P = V * I). 
            Therefore, even with a relatively low current, the high voltage results in a significant power requirement.
        '''
        current_draw = required_battery_power / required_voltage  # in amperes

        return Tr_cruise, Pr_cruise, required_rpm, required_battery_power, required_voltage, current_draw