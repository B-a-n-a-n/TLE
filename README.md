This script will create file 'data.txt' with times when sattelite is appearing on the sky and plots in created dirrectories for each day with each data.

-----------------------------------------
Copy and run this somevere if you want to download tle data:

import numpy as np
import matplotlib.pyplot as plt
from pyorbital.orbital import Orbital, get_observer_look
import pyorbital
import datetime
import os

program_path = os.path.realpath(__file__)

pyorbital.tlefile.fetch(program_path)
------------
