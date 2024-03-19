import math

class Aerofoil:
    def __init__(self) -> None:
        self._NACA = None
        self._span = None
        self._chord = None
        self._thickness = None
        self._h_cg = None  # Center of gravity might be more specific to wings, consider if it should be here

    # Setters
    def set_span(self, n):
        self._span = n
    
    def set_chord(self, n):
        self._chord = n
    
    def set_thickness(self, n):
        self._thickness = n
    
    def set_NACA(self, NACA):
        self._NACA = NACA

    # Getters
    def get_span(self):
        return self._span
    
    def get_chord(self):
        return self._chord
    
    def get_thickness(self):
        return self._thickness
    
    def get_AR(self):
        return self._span / self._chord
    
    def get_NACA(self):
        return self._NACA
    
    # Common calculations
    # TODO: Is this formula correct?
    def find_CD_NACA(self):
        return self._NACA.find_CD()
    
    def find_CD(self, CL):
        return self.get_NACA()._Cd0 + (self.get_NACA().get_r() * (CL**2)) + ((CL**2) / (math.pi * self.get_NACA()._e * self.get_NACA()._AR))
    
    # Export vairables
    def export_variables_to_dict(self):
        """
        Exports Aerofoil variables to a dictionary.
        """
        return {
            "Span": self._span,
            "Chord": self._chord,
            "Thickness": self._thickness,
            "Center of Gravity": self._h_cg
        }
    