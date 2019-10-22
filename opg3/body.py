from numpy import sqrt
import numpy as np

class AstronomicalBody:
    def __init__(self, mass, radius, init_pos, init_speed, angle=0, propulsion=(lambda: 0)):
        self.mass = mass
        self.radius = radius
        self.pos = init_pos
        self.speed = init_speed
        self.angle = np.radians(angle)
        self.init_angle = angle
        self.propulsion = propulsion

    def speed_x(self):
        return self.speed[0]

    def speed_y(self):
        return self.speed[1]

    def speed_tot(self):
        return sqrt(self.speed[0] * self.speed[0] + self.speed[1] * self.speed[1])

    def pos_x(self):
        return self.pos[0]

    def pos_y(self):
        return self.pos[1]

    def pos_tot(self):
        return sqrt(self.pos[0] * self.pos[0] + self.pos[1] * self.pos[1])

    def set_angle(self, angle):
        self.angle = np.radians(self.init_angle+angle)

    def angle_decomp(self):
        return np.cos(self.angle), np.sin(self.angle)

    def check_crash(self, radius):
        return self.pos_tot() < radius

    def check_too_far(self, radius):
        return self.pos_tot() > radius*100

    def state(self):
        return [0, self.pos[0], self.speed[0], self.pos[1], self.speed[1]]

    def set_state(self, state):
        self.pos = [state[1], state[3]]
        self.speed = [state[2], state[4]]

    def data(self, offset=(0, 0)):
        return "pos: [%.2f, %.2f], speed: [%.2f, %.2f], angle: %.2f" % (self.pos_x()-offset[0], self.pos_y()-offset[1], self.speed_x(), self.speed_y(), np.degrees(self.angle))