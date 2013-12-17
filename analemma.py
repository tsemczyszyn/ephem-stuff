#!/usr/bin/env python
'''
Plots the length and location of the end of a shadow cast from
the sunlight at the specified time of day for a 1 year period.
'''

import ephem
import math
import datetime as DT
from matplotlib import pyplot as plt
from matplotlib import animation

twopi = math.pi*2
loc = ephem.city('Toronto')
sun = ephem.Sun()

x = []
y = []
dates = []

days = 365
start = DT.datetime(2013, 12, 2, 23, 0, 0)
shift = DT.timedelta(days=-365)
dp = start+shift

fig = plt.figure()
ax = plt.axes()
line, = ax.plot([], [], lw=2)
line2, = ax.plot([], [], lw=2)
date_txt = ax.text(0.02, 0.90, '', transform=ax.transAxes)


def flip(a):
    '''Flips an azimuth to the opposite direction '''

    if a < math.pi:
        return a+math.pi
    elif a > twopi:
        return flip(a % twopi)
    else:
        return a-math.pi


def animate(i):
    a = x[:i]
    b = y[:i]
    line.set_linestyle('None')
    line.set_marker("o")
    line.set_color("r")
    line.set_data(a, b)
    date_txt.set_text(str(dates[i]))
    line2.set_data([0, x[i]], [0, y[i]])
    ax.relim()

    return line, line2, date_txt

for i in range(days+1):
    loc.date = ephem.Date(dp)
    sun.compute(loc)

    if sun.alt > 0:

        s_len = 1/math.tan(sun.alt)

        x.append((math.sin(flip(sun.az)))*s_len)
        y.append((math.cos(flip(sun.az)))*s_len)
        dates.append(ephem.localtime(loc.date))

    dp += DT.timedelta(days=1)

#Animated
#ax.set_xlim(min(x+[0]), max(x+[0]))
#ax.set_ylim(min(y+[0]), max(y+[0]))
#ax.grid(True)
#anim = animation.FuncAnimation(fig, animate, frames=len(x), interval=20)

#Not animated
plt.plot(x, y, 'ro')
plt.plot(0, 0, 'bo')

if y and x:
    plt.text(x[-1], y[-1], str(ephem.localtime(loc.date))
             + " " + str(math.degrees(flip(sun.az))) + " degrees", fontsize=10)
plt.grid()
plt.show()
