import logging

class Simulate():
    @staticmethod
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

        # Call plotting function
        cl_max_list = aircraft.plot_aero_curves(test_measurements["Test Alpha Range (degrees)"],
                                                test_measurements["Test Delta_e List (degrees)"],
                                                test_measurements["Test Reynolds Number"], test_measurements["Test h"])

        # NOTE: Arbitrary choice for cl max
        CL_max = cl_max_list[0]

        # PROBLEM 2
        # Find trimmed elevator angle for a range of angles of attack
        # NOTE: Print statements causes lambda function to fail; need to turn them off for P2
        aircraft.set_log_level(3)

        Cd0, K = aircraft.find_trimmed_drag_polar_coefficients(test_measurements["Test Alpha Range (degrees)"],
                                                            test_measurements["Test Reynolds Number"],
                                                            test_measurements["Test h"])

        logging.info(f"Drag Polar CL_max: {cl_max_list[0]}")
        logging.info(f"Cd0: {Cd0}, K: {K}")

        return CL_max, Cd0, K

    # Example usage:
    # run_aircraft_simulation(super_cub, test_measurements, wing_surface_area_m, tail_surface_area_m, wing_chord_m)
