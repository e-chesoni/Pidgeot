import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.optimize import curve_fit

from util.uav_logger import *
from util.helpers import *
from src.aircraft import *
from src.main_setup import *

from simulations.hw4.run import *
from simulations.hw5.run import *
from simulations.hw6.run import *

print("\n")
msg = "Welcome to UAV Sim!"
print(msg)
print("\n")

# TODO: Test imports
logging.info('Logging enabled')
logging.info(f"Log level: {logging.getLogger().getEffectiveLevel()}")
print("\n")

run_hw4_simulation()
#run_hw5_simulation()
#run_hw6_simulation()

# TODO: Find out why hw4 cd and k are now off...probs has to do with switch from in to m in calcuations in aircraft
# TODO: Add NACA_4415_flap data to NACA.json and analyze
