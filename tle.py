import numpy as np
import matplotlib.pyplot as plt
from pyorbital import astronomy
from datetime import datetime

def get_coords(utc_time, orb):
    return get_observer_look(*utc_time+moscow)

    zen = astronomy.sun_zenith_angle(utc_time, lon, lat)


# 55.7558° N, 37.6173° E
moscow = (37.61842, 55.751244, 0,156)
orb = Orbital("noaa 19")

start = date(2020, 3, 10)
end = date(2020, 3, 20)

days_count = start[2] - end[2]

for i in range(days_count):
    start[3] += 1
    t = time(10, 10)
    time = datetime.combine(start, t)
    print(get_coords(time, orb))
