import numpy as np
import matplotlib.pyplot as plt
from pyorbital.orbital import Orbital, get_observer_look
import datetime
import os

# generates fancy label for the plots in matplotlib
def label_gen(times):
    time_begin = datetime.time(times[-2].hour, times[-2].minute, times[-2].second)
    time_end = datetime.time(times[-1].hour, times[-1].minute, times[-1].second)
    return str(time_begin) + " - " + str(time_end)

# creates plot by given lists of angles
def tragectory_plot(name, az, el, label):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(np.array(el)*(2*np.pi/360),(np.array(az)*(-1) + 90))
    ax.set_rmax(90)
    ax.set_rmin(0)
    ax.set_rticks([90,60,30,0], [" "]*4)
    ax.grid(True)
    ax.set_title(label, va='bottom')
    plt.savefig(str(start + datetime.timedelta(days=days)) + "/" + name)
    fig.clear()
    plt.close(fig)

# final file with times when you can see sattelite
times_data = open('data.txt', 'w')

program_path = os.path.realpath(__file__)
dir_path = os.path.dirname(__file__)
print("Files will be stored at: ", program_path)

# ------------------------------------------------------------------- set your location and choose your sattelite
coords = {'lon': 37.61842, 'lat': 55.751244, 'alt': 0.156} # 55.7558° N, 37.6173° E

# TLE = """
# 1 33591U 09005A   22068.68742931  .00000068  00000+0  62115-4 0  9995
# 2 33591  99.1613 100.6691 0014831 107.6546 252.6245 14.12535828674362
# """.split("\n")
# orb = Orbital("sattelite", tle_file=None, line1 = TLE[1], line2 = TLE[2])
orb = Orbital("noaa 19")

# ------------------------------------------------------------------- set time period (yy, mm, dd)
start = datetime.date(2020, 3, 10)
end = datetime.date(2020, 3, 11)

diff = int(str(end - start).split()[0]) + 1
time = datetime.datetime.combine(start, datetime.time(0, 0))

size = 24*60*60 # ------------------------------------- set how many periods of time you want to analize in a day


curr_day_el, curr_day_az = [], []
i = 0

total_times = [time]

for days in range(diff):
    azim = curr_day_az + [180]*diff*size # stores azim and elev of sattelite for a day and the day before
    elev = curr_day_el + [180]*diff*size
    graph_num = 0
    try:
        os.mkdir(str(start + datetime.timedelta(days=days)))
    except:
        pass
    for periods in range(size):
        time = time + datetime.timedelta(seconds=(24*60*60/size))
        el_, az_ = orb.get_observer_look(time, coords['lon'], coords['lat'], coords['alt']) # gets coords of sattelite at current moment
        if az_ > 0:
            elev[periods+days*size] = el_
            azim[periods+days*size] = az_

        curr_day_el.append(el_)
        curr_day_az.append(az_)

        if (abs(curr_day_az[i])/curr_day_az[i] != abs(curr_day_az[i-1])/curr_day_az[i-1]):
            total_times.append(time)
            if ((abs(curr_day_az[i-1])/curr_day_az[i-1]) == 1):
                times_data.write(str(start + datetime.timedelta(days=days)) + "    " + label_gen(total_times) + "\n")
                tragectory_plot(str(start + datetime.timedelta(days=days))+ " #" + str(graph_num) + ".png", curr_day_az[0:-1], curr_day_el[0:-1], label_gen(total_times))
                print(graph_num , end = '-')
                graph_num += 1
            curr_day_el = [curr_day_el[-1]]
            curr_day_az = [curr_day_az[-1]]
            i = -1
        i += 1
    times_data.write("\n")
    print("day " + str(start + datetime.timedelta(days=days)) + " completed")
    tragectory_plot(str(start + datetime.timedelta(days=days)) + ".png", azim, elev, str(start + datetime.timedelta(days=days)))

times_data.close()

#print(*total_times, sep = '\n')