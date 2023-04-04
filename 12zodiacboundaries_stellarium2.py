import swisseph as swe
import numpy as np
import datetime

# Find borders for zodiac signs
nsteps = 100000  # Adjust this value as needed
nbodies = 10  # Number of celestial bodies considered
step = 1.0  # Time step in days
znames = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]
planets = list(range(swe.SUN, swe.PLUTO + 1))  # Planets from Sun to Pluto
flags = swe.FLG_SWIEPH | swe.FLG_SPEED

tstamps = np.linspace(0, nsteps * step, nsteps)
prevlon = np.zeros(nbodies)

currentDate = datetime.datetime(2023,3,21,5,10,0)

zodiac_boundaries = []
for i in range(1, 13):
    if i == 1:
        startlon = 0.0
    else:
        startlon = float(i - 1) * 30.0

    endlon = float(i) * 30.0
    rstart = 0.0
    rend = 0.0


for j in range(nsteps):
        for k, planet in enumerate(planets):
            t = swe.julday(currentDate.year, currentDate.month, currentDate.day, currentDate.hour + currentDate.minute / 60.0)  # Add the base Julian day
            xx, ret = swe.calc_ut(t, planet, flags)
            lon = xx[0]

            if lon < startlon and prevlon[k] > startlon:
                frac = (startlon - prevlon[k]) / (lon - prevlon[k])
                rstart = tstamps[j] - frac * step

            if lon < endlon and prevlon[k] > endlon:
                frac = (endlon - prevlon[k]) / (lon - prevlon[k])
                rend = tstamps[j] - frac * step

            prevlon[k] = lon

        if rstart > 0.0 and rend > 0.0:
            zodiac_boundaries.append((znames[i - 1], rstart, rend))
            print(f"{znames[i - 1]:s}, start: {rstart:15.8f}, end: {rend:15.8f}")
            break

        print("Zodiac boundaries:")
        for zodiac, start, end in zodiac_boundaries:
                print(f"{zodiac}, start: {start:15.8f}, end: {end:15.8f}")


