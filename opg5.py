import matplotlib.pyplot as plt
import opg4
import numpy as np
import math
# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Trenger kode for orbit, runga-kutta og saturn V (Oppgave 2,3,4)

#def acceleration(t, h, v, r = 6.378* (10 **6)):
    # Må lage en funksjon som finner arealet av tverrsnittet basert på trinn:

  #  area = Areal av tverrsnittfunk
  #   m = opg4.estimate_mass(t)
  #  acceleration = (opg4.get_thrust(t) / m) - (ForceOfGravity / m) - (air_res(h,area, v)/m)

G_constant = 6.674e-11
mass_earth = 5.9736e24
mass_moon = 7.3477e22
radius_earth = 6371e3
radius_moon = 1737.10e3
velocity_earth = [0.0, 0.0]
velocity_moon = [0.0, 1022.0]
rotation_earth = 0.4651e3
position_earth = [0.0, 0.0]
position_moon = [384399e3, 0.0]
Cd = 0.25
G = 9.81

print(opg4.get_thrust(100))

def density(height):
    if height < 11000:
        T = 288.19 - 0.00649 * height
        p = 101.29 * (T / 288.08) ** 5.256
    elif 11000 < height < 25000:
        T = 216.69
        p = 127.76 * np.exp(-0.000157 * height)
    else:
        T = 141.94 + 0.00299 * height
        p = 2.488 * (T / 216.6) ** -11.388
    return (p / T) * 3.4855

def Area(time):
    if time < 0:
        raise ValueError('Negative time values are not possible')
    elif time <= sum(opg4.stage_duration[:2]):
        return math.pi * 5.05 * 5.05
    else:
        return math.pi * 3.3 * 3.3


# CD er aerodynamisk egenskap
def air_resistance(time, height, velocity):
    return 0.5 * Cd * density(height) * Area(time) * velocity * velocity

def Fsum(time, height, velocity):
    return opg4.get_thrust(time) - G - air_resistance(height, time, velocity)

def acceleration(time, height, velocity):
    return Fsum(time, height, velocity) / opg4.estimate_mass(time)

def rocket_velocity_change(time):
    if(time % 1000 == 0):
        print('time', time)
        print("exhaust velocity: ", opg4.get_exhaust_velocity(time))
        print("total mass:", opg4.total_mass[0])
        print("estimated mass: ", opg4.estimate_mass(time))
    return opg4.get_exhaust_velocity(time)*math.log((opg4.total_mass[0]/opg4.estimate_mass(time)), math.e)

G_constant = 6.674e-11
mass_earth = 5.9736e24
mass_moon = 7.3477e22
radius_earth = 6371e3
radius_moon = 1737.10e3
velocity_earth = [0.0, 0.0]
velocity_moon = [0.0, 1022.0]
rotation_earth = 0.4651e3
position_earth = [0.0, 0.0]
position_moon = [384399e3, 0.0]
Cd = 0.25
G = 9.81

rocket_height = radius_earth # start height
p = 101325 # 1 atm
v = 0 # start speed


for time in range(1, 1300):

    # rocket_velocity = rocketVelocity(time)
    if time % 30 == 0:
        print("time", time)
        print("Rocket velocity:", rocket_velocity_change(time))


