import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.optimize import curve_fit

from util.uav_logger import *
from util.helpers import *
from src.aircraft import *
from src.setup import *

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

# Set Matplotlib logging level to suppress debug logs
logging.getLogger('matplotlib').setLevel(logging.WARNING)

run_hw4_simulation()
#run_hw5_simulation()
run_hw6_simulation()

'''
CD0 and K
-------------------------------------------------
Super Cub
Cd0: 0.020276808012452317, K: 0.07113059297128425

Highway Pursuit
CL_max: 0.8334546365556947
Cd0: 0.027703596939813693, K: 0.06970188495924658
'''