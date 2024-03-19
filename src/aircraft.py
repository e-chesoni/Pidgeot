from src.wing import *
from src.tail import *
from src.fuselage import *
from util.uav_logger import *

from collections import namedtuple
from typing import Union
import matplotlib.pyplot as plt

# colors
dark_blue = '#001219'
navy = '#005f73'
teal = '#0a9396'
aqua = '#94d2bd'
off_white = 'e9d8a6'
yellow = '#ee9b00'
orange = '#ca6702'
burnt_orange = '#bb3e03'
red = '#ae2012'
dark_red = '#9b2226'

class Aircraft:
    def __init__(self, name, wing, tail, fuselage):
        self._name = name
        self._wing = wing
        self._tail = tail
        self._fuselage = fuselage

    # Setters
    def set_i_h(self, i_h):
        self._i_h = i_h

    def set_wing_surface_area_in(self, wing_surface_area_in):
        self._wing_surface_area_in = wing_surface_area_in
    
    def set_tail_surface_area_in(self, tail_surface_area_in):
        self._tail_surface_area_in = tail_surface_area_in
    
    def set_wing_chord_in(self, wing_chord_in):
        self._wing_chord_in = wing_chord_in

    def enable_debug(self, debug):
        self._debug_enabled = debug
    
    def set_log_level(self, level):
        self._log_level = level

    # Simulation Methods
    def simulate(self, alpha_deg, del_e_deg, Re_c, h):
        required_attributes = ['_wing', '_tail', '_fuselage', '_i_h', '_tail_surface_area_in', '_wing_surface_area_in', '_wing_chord_in']
        for attr in required_attributes:
            if getattr(self, attr, None) is None:
                logging.error(f"Error: {attr} is not defined.\n")
                return

        AeroCoefficients = namedtuple('AeroCoefficients', 'CL CD CM')
        
        # WING
        CL_wing = self._wing.find_CL_NACA(deg_to_rad(alpha_deg))
        #CD_wing = self._wing.find_CD_NACA()
        CD_wing = self._wing.find_CD(CL_wing)
        CM_wing = self._wing.find_CM(h)

        # TAIL
        # NOTE: OK to use CL wing and AR to calculate epsion
        self._tail.set_epsilon(self._tail.find_epsilon(CL_wing, self._tail.get_NACA().get_e(), self._wing.get_NACA().get_AR()))
        CL_tail = self._tail.find_CL(deg_to_rad(alpha_deg), deg_to_rad(del_e_deg), self._i_h)
        #CD_tail = self._tail.find_CD_NACA()
        CD_tail = self._tail.find_CD(CL_tail)
        CM_tail = self._tail.find_CM(in_to_meters(self._tail_surface_area_in), in_to_meters(self._wing_surface_area_in), in_to_meters(self._wing_chord_in), CL_tail)

        # FUSELAGE
        CD_fuselage = self._fuselage.find_CD(Re_c, in_to_meters(self._wing_chord_in))
        # NOTE: adjust super_cub_fuselage volume by * 1/3 for taper
        volume_taper_percent = (1/3)
        CM_fuselage = self._fuselage.find_CM(deg_to_rad(alpha_deg), in_to_meters(self._wing_surface_area_in), in_to_meters(self._wing_chord_in), volume_taper_percent)

        CL = CL_wing + CL_tail
        CD = CD_wing + CD_tail + CD_fuselage
        CM = CM_wing + CM_tail + CM_fuselage

        if self._log_level == 1:
            wing_info = {
                "Wing Span": self._wing.get_span(),
                "Wing Chord": self._wing.get_chord(),
                "Wing Center of Gravity": self._wing.get_center_of_gravity(),
                "CL Wing": CL_wing,
                "CD Wing": CD_wing,
                "CM Wing": CM_wing
            }
            NACA_2415_info = self._wing.get_NACA().export_variables_to_dict()

            tail_info = {
                "Tail Span": self._tail.get_span(),
                "Tail Chord": self._tail.get_chord(),
                "Tail Epsilon": self._tail.get_epsilon(),
                "Tail Tau": self._tail.get_tau(),
                "CL Tail": CL_tail,
                "CD Tail": CD_tail,
                "CM Tail": CM_tail,
            }
            NACA_0009_info = self._tail.get_NACA().export_variables_to_dict()

            fuselage_info = {
                "Fuselage Length": self._fuselage.get_length(),
                "Fuselage Height": self._fuselage.get_height(),
                "CD Fuselage": CD_fuselage,
                "CM Fuselage": CM_fuselage,
            }
            
            print_info_table(NACA_2415_info, "NACA 2415 INFORMATION")
            print_info_table(wing_info, "WING INFORMATION")
            print_info_table(NACA_0009_info, "NACA 0009 INFORMATION")
            print_info_table(tail_info, "TAIL INFORMATION")
            print_info_table(fuselage_info, "FUSELAGE INFORMATION")
        
        elif self._log_level == 2:
            #logging.info(f"Total CL: {CL}")
            logging.info(f"Total CD: {CD}")
            #logging.info(f"Total CM: {CM}")

        # NOTE: PAY ATTENTION TO RETURN ORDER HERE!!
        return AeroCoefficients(CL=CL, CD=CD, CM=CM)
    
    # Plotting
    def plot_aero_curves(self, alpha_range, del_e_degs, Re_c, h):
        """
        Plots CL vs alpha and CL vs CD curves for a range of angle of attack values and elevator deflection angles with custom line colors.
        Additionally, plots CM vs alpha on the same graph as CL vs alpha using a secondary y-axis.

        Parameters:
        - alpha_range (numpy.ndarray): An array of angle of attack values in degrees.
        - del_e_degs (list of float): List of elevator deflection angles in degrees.
        - Re_c (float): Reynolds number based on the chord length.
        - h (float): Altitude.
        """
        # Define a list of colors for the plots
        palette_1 = [dark_blue, navy, teal]
        palette_2 = [yellow, burnt_orange, dark_red]
        
        plt.figure(figsize=(12, 12))

        # Plot CL vs alpha for different del_e_deg values
        ax1 = plt.subplot(2, 1, 1)  # Set primary axis to CL
        ax2 = ax1.twinx()  # Set secondary axis to CM
        
        for i, del_e_deg in enumerate(del_e_degs):
            CL_values = []
            CD_values = []
            CM_values = []
            for alpha_deg in alpha_range:
                CL, CD, CM = self.simulate(alpha_deg, del_e_deg, Re_c, h)
                CL_values.append(CL)
                CD_values.append(CD)
                CM_values.append(CM)
            
            # Cycle through colors
            color1 = palette_1[i % len(palette_1)]
            color2 = palette_2[i % len(palette_1)]
            ax1.plot(alpha_range, CL_values, '-o', label=f'CL vs Alpha, del_e={del_e_deg}', color=color1)
            ax2.plot(alpha_range, CM_values, '--', label=f'CM vs Alpha, del_e={del_e_deg}', color=color2)
        
        ax1.set_xlabel('Alpha (degrees)')
        ax1.set_ylabel('CL (Lift Coefficient)', color=dark_blue)
        ax2.set_ylabel('CM (Moment Coefficient)', color=red)
        ax1.set_title('Lift Coefficient (CL) and Moment Coefficient (CM) vs. Angle of Attack (Alpha) for different elevator deflections')
        ax1.grid(True)
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Set the y-axis limits for both CL and CM to range from -1 to 2
        ax1.set_ylim([-2, 2.5])
        ax2.set_ylim([-2, 2.5])

        # Plot CL vs CD for different del_e_deg values
        plt.subplot(2, 1, 2)
        for i, del_e_deg in enumerate(del_e_degs):
            CL_values = []
            CD_values = []
            for alpha_deg in alpha_range:
                CL, CD, CM = self.simulate(alpha_deg, del_e_deg, Re_c, h)
                CL_values.append(CL)
                CD_values.append(CD)
            
            color = palette_1[i % len(palette_1)]
            plt.plot(CD_values, CL_values, '-o', label=f'CL vs CD, del_e={del_e_deg}', color=color)
        
        plt.xlabel('CD (Drag Coefficient)')
        plt.ylabel('CL (Lift Coefficient)')
        plt.title('Lift Coefficient (CL) vs. Drag Coefficient (CD) for different elevator deflections')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.show()