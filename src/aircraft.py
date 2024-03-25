from src.wing import *
from src.tail import *
from src.fuselage import *
from util.uav_logger import *
from src.main_setup import *

from collections import namedtuple
from typing import Union
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.optimize import curve_fit

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
    def __init__(self, name, wing, tail, fuselage, units):
        logging.info(f"Aircraft named \"{name}\" created")
        self._name = name
        self._units = units
        self._wing = wing
        self._tail = tail
        self._fuselage = fuselage
    
    # Logging
    def enable_debug(self, debug):
        self._debug_enabled = debug
    
    def set_log_level(self, level):
        self._log_level = level
    
    # Getters
    def get_W0(self):
        return self._W0
    
    def get_Wp(self):
        return self._Wp
    
    def get_wing_surface_area_m(self):
        return self._wing_surface_area_m
    
    # Setters
    def set_units(self, units):
        self._units = units

    def set_i_h(self, i_h):
        self._i_h = i_h

    def set_wing_surface_area_in(self, wing_surface_area_in):
        self._wing_surface_area_in = wing_surface_area_in
        self._wing_surface_area_m = in_to_meters(wing_surface_area_in)
    
    def set_wing_surface_area_m(self, wing_surface_area_m):
        self._wing_surface_area_m = wing_surface_area_m
    
    def set_tail_surface_area_in(self, tail_surface_area_in):
        self._tail_surface_area_in = tail_surface_area_in
        self._tail_surface_area_m = in_to_meters(tail_surface_area_in)
    
    def set_tail_surface_area_m(self, tail_surface_area_m):
        self._tail_surface_area_m = tail_surface_area_m
    
    def set_wing_chord_in(self, wing_chord_in):
        self._wing_chord_in = wing_chord_in
        self._wing_chord_m = in_to_meters(wing_chord_in)

    def set_wing_chord_m(self, wing_chord_m):
        self._wing_chord_m = wing_chord_m

    def set_weight(self, weight):
        self._weight = weight

    def set_critical_angle_of_attack(self, crit_angle):
        self._critical_angle_of_attack = crit_angle
    
    def set_trimmed_drag_polar_coefficients(self, Cd0, K):
        self._Cd0 = Cd0
        self._K = K

    # We = wmpty weight
    def set_We_over_W0(self, val):
        self._We_over_W0 = val
    
    # Wf = fuel weight
    def set_Wf_over_W0(self, val):
        self._Wf_over_W0 = val
    
    # Wp = payload weight
    def set_Wp(self, Wp):
        self._Wp = Wp
    
    def set_W0(self, W0):
        self._W0 = W0

    # Simulation Methods
    
    def simulate(self, alpha_deg, del_e_deg, Re_c, h):
        
        required_attributes = ['_wing', '_tail', '_fuselage', '_i_h', '_tail_surface_area_m', '_wing_surface_area_m', '_wing_chord_m']
        for attr in required_attributes:
            if getattr(self, attr, None) is None:
                logging.error(f"Error: {attr} is not defined.\n")
                return

        AeroCoefficients = namedtuple('AeroCoefficients', 'CL CD CM')
        
        # WING
        alpha_rad = deg_to_rad(alpha_deg)
        critical_alpha_rad = deg_to_rad(self._critical_angle_of_attack)
        
        CL_wing = self._wing.find_CL_NACA(alpha_rad)

        # TODO: Still working on this...
        '''    
        # Adjust CL calculation for stall behavior
        if alpha_rad <= critical_alpha_rad:
            CL_wing = self._wing.find_CL_NACA(alpha_rad)
        else:
            # Simplified stall behavior: CL starts to decrease or remains constant
            # This is a placeholder; adjust based on your stall model
            #decrease_factor = 5 * (alpha_rad - critical_alpha_rad)
            decrease_factor = 0
            CL_wing = self._wing.find_CL_NACA(critical_alpha_rad) - decrease_factor
        '''

        CD_wing = self._wing.find_CD(CL_wing)
        CM_wing = self._wing.find_CM(h)

        # TAIL
        # NOTE: OK to use CL wing and AR to calculate epsion
        # TODO: Look for in to m errors here
        self._tail.set_epsilon(self._tail.find_epsilon(CL_wing, self._tail.get_NACA().get_e(), self._wing.get_NACA().get_AR()))
        CL_tail = self._tail.find_CL(deg_to_rad(alpha_deg), deg_to_rad(del_e_deg), self._i_h)
        CD_tail = self._tail.find_CD(CL_tail)
        CM_tail = self._tail.find_CM(self._tail_surface_area_m, self._wing_surface_area_m, self._wing_chord_m, CL_tail)
        
        # FUSELAGE
        CD_fuselage = self._fuselage.find_CD(Re_c, self._wing_chord_m)
        # NOTE: adjust super_cub_fuselage volume by * 1/3 for taper
        volume_taper_percent = (1/3)
        CM_fuselage = self._fuselage.find_CM(deg_to_rad(alpha_deg), self._wing_surface_area_m, self._wing_chord_m, volume_taper_percent)

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
            logging.info(f"Total CL: {CL}")
            logging.info(f"Total CD: {CD}")
            logging.info(f"Total CM: {CM}")

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

        cl_max_list = []
        
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
            
            # Find CL_max and corresponding alpha
            CL_max = max(CL_values)
            alpha_at_CL_max = alpha_range[CL_values.index(CL_max)]
            
            # Cycle through colors
            color1 = palette_1[i % len(palette_1)]
            color2 = palette_2[i % len(palette_1)]
            #ax1.plot(alpha_range, CL_values, '-o', label=f'CL vs Alpha, del_e={del_e_deg}', color=color1)

            # Plotting modifications
            ax1.plot(alpha_range, CL_values, '-o', label=f'CL vs Alpha, del_e={del_e_deg}', color=color1)
            # Add critical angle of attack marker
            crit_angle = self._critical_angle_of_attack
            ax1.axvline(x=crit_angle, color='grey', linestyle='--', label='Critical Angle of Attack')
            # Find the index of the closest alpha value to the critical angle
            #crit_index = np.abs(alpha_range - crit_angle).argmin()

            # For each del_e_deg, find CL at the critical angle
            for i, del_e_deg in enumerate(del_e_degs):
                CL_at_crit_angle = self.simulate(crit_angle, del_e_deg, Re_c, h)[0]
                cl_max_list.append(CL_at_crit_angle)
                # Highlight CL at the critical angle on the plot
                ax1.plot(crit_angle, CL_at_crit_angle, 'x', color='red', label=f'CL at Crit Angle, del_e={del_e_deg}')

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

        return cl_max_list

    def find_trimmed_drag_polar_coefficients(self, alpha_range, Re_c, h):
        trimmed_data = []
        for alpha_deg in alpha_range:
            f_CM = lambda del_e_deg: self.simulate(alpha_deg, del_e_deg, Re_c, h)[-1]  # Access CM directly
            print(f_CM)
            del_e_deg_trim = fsolve(f_CM, 0)[0]
            # Now unpack the returned values in the order of CL, CD, CM
            result = self.simulate(alpha_deg, del_e_deg_trim, Re_c, h)
            CL, CD, CM = result.CL, result.CD, result.CM
            trimmed_data.append((CM, CL, CD))

        # Extract CL and CD for curve fitting
        CL_data = [data[1] for data in trimmed_data]
        CD_data = [data[2] for data in trimmed_data]

        # Fit the parabolic drag polar equation
        def drag_polar(CL, Cd0, K):
            return Cd0 + K * CL**2

        popt, pcov = curve_fit(drag_polar, CL_data, CD_data)
        Cd0, K = popt

        return Cd0, K

    def find_trimmed_CL(self, V, weight, rho):
        g = 9.81
        return (2 * weight * g) / (rho * V**2 * self._wing_surface_area_m) # TODO: why does changing this form in to m not change cd0/k?

    def find_trimmed_drag(self, CL):
        return self._Cd0 + self._K * CL**2
    
    def find_thrust_power(self, V, rho):
        trimmed_CL = self.find_trimmed_CL(self._weight, rho, V)
        trimmed_CD = self.find_trimmed_drag(trimmed_CL)
        D = 0.5 * rho * V**2 * self._wing_surface_area_m * trimmed_CD  # Drag = Thurst
        P = D * V  # Power
        return D, P
    
    def plot_thrust_and_power(self, rho, V_range):
        thrust = []
        power = []
        
        for V in V_range:
            T, P = self.find_thrust_power(V, rho)
            thrust.append(T)
            power.append(P)

        # Plotting
        fig, ax1 = plt.subplots()

        ax1.set_xlabel('Velocity (m/s)')
        ax1.set_ylabel('Thrust (N)', color=navy)
        ax1.plot(V_range, thrust, color=navy)
        ax1.tick_params(axis='y', labelcolor=navy)
        # Invert the y-axis for thrust
        #ax1.invert_yaxis()

        ax2 = ax1.twinx() # instantiate a second axes that shares the same x-axis

        ax2.set_ylabel('Power (W)', color=burnt_orange)  # we already handled the x-label with ax1
        ax2.plot(V_range, power, color=burnt_orange)
        ax2.tick_params(axis='y', labelcolor=burnt_orange)
        # Invert the y-axis for power
        #ax2.invert_yaxis()

        # Find min thrust required and corresponding velocity
        min_thrust = min(thrust)
        min_speed_index = thrust.index(min_thrust)
        min_speed = V_range[min_speed_index]

        plt.title(f'Thrust vs Power for Level Flight')
        fig.tight_layout()  # fix y axis clipping

        plt.show()

    def find_Wf_over_W0(self, Range, H_F, L_over_d, eta_p):
        return ( Range / H_F ) * ( 1 / L_over_d ) * ( 1 / eta_p)
    
    def find_total_weight(self):
        return ( self._Wp / (1 - self._Wf_over_W0 - self._We_over_W0))
    
    def find_Wp(self):
        print(self._Wf_over_W0)
        print(self._We_over_W0)
        return (1 - self._Wf_over_W0 - self._We_over_W0) * self._W0
    
    def find_wing_surface_area(self, rho, V, CL):
        g = 9.81
        return ( ( 2 * self._W0 * g) / ( rho * (V**2) * CL ) )
    
    def calculate_wing_dimensions_m(self):
        # Define a l/w ratio for the wing
        length_to_width_ratio = 3  # This means the length is 3 times the width

        # area = length * width, so width = sqrt(area / ratio)
        width = math.sqrt(self._wing_surface_area_m / length_to_width_ratio)

        # find length
        length = width * length_to_width_ratio

        return length, width

