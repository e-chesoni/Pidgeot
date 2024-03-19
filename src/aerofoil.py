class Aerofoil:
    def __init__(self) -> None:
        self.NACA = None
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
        self.NACA = NACA

    # Getters
    def get_span(self):
        return self._span
    
    def get_chord(self):
        return self._chord
    
    def get_thickness(self):
        return self._thickness
    
    def get_AR(self):
        return self._span / self._chord
    
    # Common calculations
    # TODO: Is this formula correct?
    def find_CD_NACA(self):
        return self.NACA.find_CD()
    
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
    