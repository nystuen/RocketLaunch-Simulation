from opg_5.opg5 import *
from helper_classes.rungekutta import *
from opg_4.opg4 import *

gravity = 0
thrust = 0
airResistance = 0
speed = 0

"""
Orbit Class

init_state is [t0,x0,vx0,y0,vx0],
where (x0,y0) is the initial position
, (vx0,vy0) is the initial velocity
and t0 is the initial time
"""
"""
Orbit Class

init_state is [t0,x0,vx0,y0,vx0],
where (x0,y0) is the initial position
, (vx0,vy0) is the initial velocity
and t0 is the initial time
"""


class Orbit:
    GravConstant = 6.67408 * 10 ** (-11)
    M_e = 5.972 * 10 ** 24
    M_m = 7.34767309 * 10 ** 22
    h = 0.000001
    tol = 05e-10
    prevPositions = [[0], [384400000]]

    def __init__(self,
                 init_state,
                 task,
                 G=GravConstant,
                 m1=M_e,
                 m2=M_m,
                 ):
        self.GravConst = G
        self.mPlanet1 = m1
        self.mPlanet2 = m2
        self.state = np.asarray(init_state, dtype='float')
        if task == 3:
            self.rkf54 = RungeKuttaFehlberg54(self.ydotTask3, len(self.state), self.h, self.tol)
            self.prevPositions = self.prevPositions
        elif task == 5:
            self.rkf54 = RungeKuttaFehlberg54(self.ydotTask5, len(self.state), self.h, self.tol)
            self.prevPositions = self.prevPositions
        elif task == 6:
            self.rkf54 = RungeKuttaFehlberg54(self.ydotTask6, len(self.state), self.h, self.tol)
            self.prevPositions = [[0], [6371010]]
        self.check = 0

    def getPos(self):
        return self.prevPositions

    def addPos(self, x, y):
        self.prevPositions[0].append(x)
        self.prevPositions[1].append(y)

    def position(self):
        """compute the current x,y positions of the pendulum arms"""
        x1 = self.state[1]
        y1 = self.state[3]
        x2 = self.state[5]
        y2 = self.state[7]
        return (x1, y1), (x2, y2)

    def energy(self):
        pxJ = self.state[1]
        vxJ = self.state[2]
        pyJ = self.state[3]
        vyJ = self.state[4]
        pxR = self.state[5]
        vxR = self.state[6]
        pyR = self.state[7]
        vyR = self.state[8]
        m_earth = self.mPlanet1
        G = self.GravConst
        mR = estimate_mass(self.state[0])
        dist = np.sqrt((pxR - pxJ) ** 2 + (pyR - pyJ) ** 2)
        uTot = -G * m_earth * mR / dist
        k_earth = m_earth * (vxJ ** 2 + vyJ ** 2) / 2
        kR = mR * (vxR ** 2 + vyR ** 2) / 2
        return (k_earth + uTot + kR) / (10 ** 24)

    def energyTask3(self):
        pxJ = self.state[1]
        vxJ = self.state[2]
        pyJ = self.state[3]
        vyJ = self.state[4]
        pxM = self.state[5]
        vxM = self.state[6]
        pyM = self.state[7]
        vyM = self.state[8]
        m_earth = self.mPlanet1
        m_moon = self.mPlanet2
        G = self.GravConst
        dist = np.sqrt((pxM - pxJ) ** 2 + (pyM - pyJ) ** 2)
        uTot = -G * m_earth * m_moon / dist
        k_earth = m_earth * (vxJ ** 2 + vyJ ** 2) / 2
        k_moon = m_moon * (vxM ** 2 + vyM ** 2) / 2
        return (k_earth + uTot + k_moon) / (10 ** 24)

    def time_elapsed(self):
        return self.state[0]

    def step(self):
        w0 = self.state
        self.state, E = self.rkf54.safeStep(w0)

    def ydotTask5(self, x):
        m_earth = self.mPlanet1
        pxJ = x[1]
        vxJ = x[2]
        pyJ = x[3]
        vyJ = x[4]
        pxR = x[5]
        vxR = x[6]
        pyR = x[7]
        vyR = x[8]

        z = np.zeros(9)
        z[0] = 1
        z[1] = 0
        z[2] = 0
        z[3] = 0
        z[4] = 0
        z[5] = 0
        z[6] = 0
        z[7] = vyR
        z[8] = acceleration(x[0], pyR - pyJ, vyR)
        return z

    def ydotTask3(self, x):
        m_earth = self.mPlanet1
        m_moon = self.mPlanet2
        pxJ = x[1]
        vxJ = x[2]
        pyJ = x[3]
        vyJ = x[4]
        pxM = x[5]
        vxM = x[6]
        pyM = x[7]
        vyM = x[8]

        z = np.zeros(9)
        dist = np.sqrt((pxM - pxJ) ** 2 + (pyM - pyJ) ** 2)
        z[0] = 1
        z[1] = vxJ
        z[2] = (self.GravConst * m_moon * (pxM - pxJ)) / (dist ** 3)
        z[3] = vyJ
        z[4] = (self.GravConst * m_moon * (pyM - pyJ)) / (dist ** 3)
        z[5] = vxM
        z[6] = (self.GravConst * m_earth * (pxJ - pxM)) / (dist ** 3)
        z[7] = vyM
        z[8] = (self.GravConst * m_earth * (pyJ - pyM)) / (dist ** 3)
        return z

    def getValues(self):
        pxJ = self.state[1]
        vxJ = self.state[2]
        pyJ = self.state[3]
        vyJ = self.state[4]
        pxR = self.state[5]
        vxR = self.state[6]
        pyR = self.state[7]
        vyR = self.state[8]

        values = np.zeros(5)
        values[0] = np.sqrt(vxR ** 2 + vyR ** 2)
        values[1] = dist = np.sqrt((pxR - pxJ) ** 2 + (pyR - pyJ) ** 2)
        values[2] = vxR
        values[3] = vyR

        return values

    def ydotTask6(self, x):
        m_earth = self.mPlanet1
        pxJ = x[1]
        vxJ = x[2]
        pyJ = x[3]
        vyJ = x[4]
        pxR = x[5]
        vxR = x[6]
        pyR = x[7]
        vyR = x[8]

        dist = np.sqrt((pxR - pxJ) ** 2 + (pyR - pyJ) ** 2)

        angle_V = np.arctan(vyR / vxR)
        angle_R = np.arcsin(pyR / dist)

        if (pxR > 0 and pyR > 0):
            angle_R = np.arcsin(pyR / dist)
        elif (pxR < 0 and pyR < 0):
            angle_R = - np.pi / 2 - (np.pi / 2 + np.arcsin(pyR / dist))
        elif (pxR < 0 and pyR > 0):
            angle_R = np.pi - np.arcsin(pyR / dist)

        stage = get_stage(x[0])

        if x[0] < 60:
            angle_F = np.pi / 2
        else:
            angle_F = angle_V - (0.034) * stage ** 2

        gravity = rocket_gravity(dist, estimate_mass(x[0]))
        speed = np.sqrt(vxR ** 2 + vyR ** 2)
        thrust = get_thrust(x[0])
        airResistance = air_resistance(dist, speed, x[0])

        z = np.zeros(9)
        z[0] = 1
        z[1] = 0
        z[2] = 0
        z[3] = 0
        z[4] = 0
        z[5] = vxR
        ax = (gravity * np.cos(angle_R + np.pi) + airResistance * np.cos(angle_V + np.pi) + thrust * np.cos(
            angle_F)) / estimate_mass(x[0])
        z[6] = ax
        z[7] = vyR
        ay = (gravity * np.sin(angle_R + np.pi) + airResistance * np.sin(angle_V + np.pi) + thrust * np.sin(
            angle_F)) / estimate_mass(x[0])
        z[8] = ay

        return z
