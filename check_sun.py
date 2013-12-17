#!/usr/bin/env python
'''
Finds the times in which the sun will be shining at my desk
through the skylight.
'''
import ephem
import math
import datetime as DT


def format_timedelta(tdelta):

    seconds = tdelta.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return '%02d:%02d' % (hours, minutes)

loc = ephem.city('Toronto')
sun = ephem.Sun()

days = 365
start = DT.datetime(2015, 1, 1, 0, 0, 0)
shift = DT.timedelta(days=-365)
dp = start+shift

dates = dict()

for i in range(days+1):
    loc.date = ephem.Date(dp)
    times = []

    for j in range(1439):
        mins = DT.timedelta(minutes=j+1)
        loc.date = ephem.Date(dp+mins)
        sun.compute(loc)

        if 45 < math.degrees(sun.alt) < 47:
            if 145 < math.degrees(sun.az) < 155:
                d = ephem.Date(ephem.localtime(loc.date)).datetime()
                times.append(d.time())
                dates[str(d.date())] = times

    dp += DT.timedelta(days=1)

print "Dates and Times for Sunlight at my desk\n"
print "Date - Time Range - Duration"
print "---------------------------------------"

for d in iter(sorted(dates.keys())):
    start = min(dates[d])
    end = max(dates[d])
    duration = DT.datetime.combine(DT.datetime.today(), end)\
        - DT.datetime.combine(DT.datetime.today(), start)

    print d + "\t" + start.strftime('%H:%M') + " - " + end.strftime('%H:%M')\
            + "\t" + format_timedelta(duration)
