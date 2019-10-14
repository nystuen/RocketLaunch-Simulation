import matplotlib.pyplot as plt

# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Index in the following arrays indicates which stage
dry_weights = [1.31e5, 3.6e4, 1e4]
total_mass = [2.970e6, 6.800e5, 1.838e5, 7.43e4]
fuel_mass = [2.169e6, 4.44e6, 1.09e6]
stage_duration = [168, 367, 494]
diameters = [10, 10, 6.604]
thrust = [3.4e7, 4.9e6, 1.0331e6]

speed = [2.3e3]
instrument_module_weight = 1996

estimated_exhaust_each_stage = []

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


def estimate_mass(time):
    if time < 0:
        return ValueError('Negative time values are not possible')
    elif time <= stage_duration[0]:
        return total_mass[0] - calculate_fuel_mass_per_second_given_time(time) * time
    elif time <= sum(stage_duration[:2]):
        return total_mass[1] - calculate_fuel_mass_per_second_given_time(time) * (time - stage_duration[0])
    elif time <= sum(stage_duration[:3]):
        return total_mass[2] - calculate_fuel_mass_per_second_given_time(time) * (time - sum(stage_duration[:2]))
    else:
        return total_mass[3]




def get_thrust(time):
    if time < 0:
        return ValueError('Negative time values are not possible')
    elif time <= stage_duration[0] - 26:
        return thrust[0]
    elif time <= stage_duration[0]:
        return thrust[0] * (4/5)
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


print("Estimated exhaust velocity each stage = %s" % estimated_exhaust_each_stage)

# Estimate masses for time and plot
estimated_masses = []
estimated_thrusts = []
for tid in range(1400):
    estimated_masses.append(estimate_mass(tid))
    estimated_thrusts.append(get_thrust(tid))

    #if tid % 1202 == 0: print(estimate_mass(tid))

#print(estimated_masses)
plt.plot(estimated_masses)
plt.ylabel('Mass (kg)')
plt.xlabel('Time (s)')
plt.show()

plt.plot(estimated_thrusts)
plt.ylabel('Thrust (N)')
plt.xlabel('Time (s)')
plt.show()

input = "123213122"
print(input.isdigit())
