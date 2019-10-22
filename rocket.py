from opg4 import *
from opg5 import *

def angle_delta(t):
    if t < 0:
        raise ValueError('Tiden kan ikke være negativ')
    elif t < 30:
        return 0
    elif t < 169:
        return (60 / 138) * (t - 30)
    elif t < 1029:
        return angle_delta(168) + (t - 168) * (60 / 860)
    else:
        return angle_delta(768)


def total_force_upwards(h, t, v):
    return total_force(h, t, v, 1e9)


def stop_engine(tid):
    return lambda h, t, v: total_force(h, t, v, tid)


def total_force(h, t, v, tid):
    if t > tid:
        return 0, air_resistance(h, t, v)/estimate_mass(t)
    return get_thrust(t) / estimate_mass(t), air_resistance(h, t, v) / estimate_mass(t)