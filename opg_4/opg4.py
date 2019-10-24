import matplotlib.pyplot as plt

# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Index in the following arrays indicates which stage
dry_weights = [131000, 40100, 13500]
total_mass = [2909200, 619200, 123000, 13500]
fuel_mass = [2.169e6, 4.44e5, 1.09e5]
stage_duration = [168, 360, 165]
diameters = [10, 10, 6.604]
thrust = [35100000, 5141000, 1000000]

estimated_exhaust_each_stage = []


def get_stage(time):
    if time < 0:
        return 0
    elif time <= stage_duration[0]:
        return 1
    elif time <= sum(stage_duration[:2]):
        return 2
    elif time <= sum(stage_duration[:3]):
        return 3
    else:
        return 4


def stageIsInvalid(stage):
    if stage != 1 and stage != 2 and stage != 3:
        return True
    else:
        return False


def calculate_fuel_mass_per_second(stage):
    if stageIsInvalid(stage): return ValueError('Stage does not exists')
    return fuel_mass[stage - 1] / stage_duration[stage - 1]


def calculate_fuel_mass_per_second_given_time(time):
    if time < 0:
        return ValueError('Negative time values are not possible')
    elif time <= stage_duration[0]:
        return calculate_fuel_mass_per_second(1)
    elif time <= sum(stage_duration[:2]):
        return calculate_fuel_mass_per_second(2)
    elif time <= sum(stage_duration[:3]):
        return calculate_fuel_mass_per_second(3)
    else:
        return 0


def estimate_exhaust_velocity(thrust, stage):
    m = calculate_fuel_mass_per_second(stage)
    v = thrust / m
    return v


def get_exhaust_velocity(time):
    if time < 0:
        return ValueError('Negative time values are not possible')
    elif time <= stage_duration[0]:
        return estimate_exhaust_velocity(get_thrust(time), 1)
    elif time <= sum(stage_duration[:2]):
        return estimate_exhaust_velocity(get_thrust(time), 2)
    elif time <= sum(stage_duration[:3]):
        return estimate_exhaust_velocity(get_thrust(time), 3)
    else:
        return 0


def estimate_mass(time):
    if time < 0:
        return ValueError('Negative time values are not possible')
    elif (get_stage(time) == 1):
        return total_mass[0] - calculate_fuel_mass_per_second_given_time(time) * time
    elif (get_stage(time) == 2):
        return total_mass[1] - calculate_fuel_mass_per_second_given_time(time) * (time - stage_duration[0])
    elif (get_stage(time) == 3):
        return total_mass[2] - calculate_fuel_mass_per_second_given_time(time) * (time - sum(stage_duration[:2]))
    else:
        return total_mass[3]


def get_thrust(time):
    if time < 0:
        return ValueError('Negative time values are not possible')
    elif time <= stage_duration[0] - 26:
        return thrust[0]
    elif time <= stage_duration[0]:
        return thrust[0] * (4 / 5)
    elif time <= stage_duration[0] + 10:
        return 0
    elif time <= sum(stage_duration[:2]):
        return thrust[1]
    elif time <= sum(stage_duration[:3]):
        return thrust[2]
    else:
        return 0


# Estimate exhaust velocity in each stage and fill array
for stage in range(len(stage_duration)):
    estimated_exhaust_velocity = estimate_exhaust_velocity(thrust[stage], (stage + 1))
    estimated_exhaust_each_stage.append(estimated_exhaust_velocity)

print('exhaust each stage:', estimated_exhaust_each_stage)
