from util.helpers import *
from util.uav_logger import *

class NACA():
    def __init__(self, wing_type, Cd, CL, Cd0, alpha_0, AR, e) -> None:
        # PRIVATE VARIABLES
        # Assigned
        self._wing_type = wing_type
        self._Cd = Cd
        self._CL = CL
        self._Cd0 = Cd0
        self._alpha_0 = alpha_0
        self._AR = AR
        self._e = e
        # Unassigned
        self._CM_aero_center = None
        self._CL_start = None
        self._CL_end = None
        self._alpha_start = None
        self._alpha_end = None

    # Setters
    def set_CL_window(self, CL_start, CL_end):
        self._CL_start = CL_start
        self._CL_end = CL_end

    def set_alpha_window(self, alpha_start, alpha_end):
        self._alpha_start = alpha_start
        self._alpha_end = alpha_end
    
    def set_CM_aero_center(self, CM_aero_center):
        self._CM_aero_center = CM_aero_center

    # Getters
    def get_Cd(self):
            return self._Cd

    def get_CL(self):
        return self._CL

    def get_Cd0(self):
        return self._Cd0
    
    def get_alpha_0(self):
        return self._alpha_0

    def get_AR(self):
        return self._AR

    def get_r(self):
        return ((self._Cd * self._CL) - self._Cd0) / self._CL**2
    
    def get_e(self):
        return self._e
    
    def get_CM_aero_center(self):
        return self._CM_aero_center

    # Calculations
    def find_a2D(self):
        # Check if any of the required variables is None
        if None in (self._CL_start, self._CL_end, self._alpha_start, self._alpha_end):
            logging.error("CL start and end or alpha start and end not set")
            return None
        else:
            return (self._CL_end - self._CL_start) / (deg_to_rad(self._alpha_end - self._alpha_start))

    def find_a3D(self):
        return self.find_a2D() / (1 + (self.find_a2D() / (math.pi * self.get_AR())))
    
    def find_CD(self):
        return self.get_Cd0() + (self.get_r() * (self.get_CL()**2)) + ((self.get_CL()**2) / (math.pi * self.get_e() * self.get_AR()))
    
    def find_CL(self, alpha):
        return self.find_a3D() * (alpha - self.get_alpha_0())
    
    # Export params
    def export_variables_to_dict(self):
        """
        Exports NACA variables to a dictionary.
        """
        return {
            "Wing Type": self._wing_type,
            "Cd": self._Cd,
            "CL": self._CL,
            "Cd0": self._Cd0,
            "Alpha_0": self._alpha_0,
            "AR": self._AR,
            "e": self._e,
            "CM Aero Center": self._CM_aero_center,
            "CL Start": self._CL_start,
            "CL End": self._CL_end,
            "Alpha Start": self._alpha_start,
            "Alpha End": self._alpha_end
        }

    # Print params
    def print_parameters(self, debug):
        if debug:
            # Prepare messages for each parameter, showing "None" if the parameter is not set
            cd_msg = f"Cd: {self._Cd}" if self._Cd is not None else "Cd: None"
            cl_msg = f"CL: {self._CL}" if self._CL is not None else "CL: None"
            cd0_msg = f"Cd0: {self._Cd0}" if self._Cd0 is not None else "Cd0: None"
            alpha_0_msg = f"alpha_0: {self._alpha_0}" if self._alpha_0 is not None else "alpha_0: None"
            ar_msg = f"AR: {self._AR}" if self._AR is not None else "AR: None"
            e_msg = f"e: {self._e}" if self._e is not None else "e: None"
            cm_aero_center_msg = f"CM aero center: {self.get_CM_aero_center()}" if self.get_CM_aero_center() is not None else "CM aero center: None"
    
            # Combine all messages into one log entry
            logging.info(f"NACA {self._wing_type} parameters: {cd_msg}, {cl_msg}, {cd0_msg}, "
                         f"{alpha_0_msg}, {ar_msg}, {e_msg}, {cm_aero_center_msg}")
        else:
            logging.info("Debug set to off.")

