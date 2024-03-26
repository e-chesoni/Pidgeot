import numpy as np
from enum import Enum

# Define the units enum
class Units(Enum):
    INCHES = "in"
    CENTIMETERS = "cm"
    METERS = "m"
    FEET = "ft"

# Test Measurements
# NOTE: Define test measurements in a dictionary
test_measurements = {
    "Test Alpha (degrees)": 30, # NOTE: for main impl: alpha range -30 to 30 (-0.524 - 0.524 in rads) intervals of 5
    "Test Alpha Range (degrees)": np.linspace(-10, 30, 21),
    "Test Delta_e (degrees)": 20,
    "Test Delta_e List (degrees)": [0, 5, 10],
    "Test Reynolds Number": 6e5,
    "Test h": 0.25,
    "Test i_h (meters)": 0,
    "Test Critical Angle of Attack (degrees)": 12,
    "Test Velocity Range (m/s)": np.linspace(0, 30, 100),
    "Test Air Density (kg/m^3)": 1.225,
}