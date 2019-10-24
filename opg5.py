# !/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import opg4
import numpy as np
import math

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
G_k = 6.67 * 10**(-11)

def Area(time):
    if opg4.get_stage(time) == 0 or opg4.get_stage(time) == 1 or opg4.get_stage(time == 2):
        return np.pi * 5.05 * 5.05
    else:
        return np.pi * 3.3 * 3.3

def air_resistance( height, velocity,time):
    height -= radius_earth
    return 0.5 * Cd * density(height) * Area(time) * velocity * velocity


def density(height):

    if height < 11000:
        T = 288.19 - 0.00649 * height
        p =101290* (T / 288.08) ** 5.256
    elif 11000 < height < 25000:
        T = 216.69
        p = 127760 * np.exp(-0.000157 * height)
    elif height < 100000:
        T = 141.94 + 0.00299 * height
        p = 2488 * (T / 216.6) ** -11.388
    else:
        p = 0
        T = 2.7
    return (p / T) * 0.0034855

def Fsum(time, height, velocity):
    return opg4.get_thrust(time) - rocket_gravity(height, opg4.estimate_mass(time)) - air_resistance(height, time, velocity)

def acceleration(time, height, velocity):
    return Fsum(time, height, velocity) / opg4.estimate_mass(time)

def rocket_velocity_change(time):
    return opg4.get_exhaust_velocity(time)*math.log((opg4.total_mass[0]/opg4.estimate_mass(time)), math.e)

def rocket_gravity(distance, mass):
    return G_constant * mass_earth * mass / (distance ** 2)
