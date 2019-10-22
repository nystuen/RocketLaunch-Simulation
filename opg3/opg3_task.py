from opg3.orbit import *
from animation import *
from opg4 import *
from opg5 import *
import time


start_time = time.time()
resolution = 15
imagescaling = 20

orbit = OrbitSatellite(G, AstronomicalBody(mass_earth, radius_earth, position_earth, velocity_earth),
                       AstronomicalBody(mass_moon, radius_moon, position_moon, velocity_moon), tol=5e-14)

# graph_satellite_path(orbit, 1000, 28 * 86400)
animate_two_bodies_3d(orbit, imagescaling, resolution, radius_earth, radius_moon, position_moon[0]/1.5,
                      86400, seconds=28, filnavn="test3", angle=(30, 90), movie=True)

# kommenter ut noen av metodene for å ikke kjøre alle etter hverandre