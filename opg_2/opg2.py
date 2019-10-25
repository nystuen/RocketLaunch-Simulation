from helper_classes.rungekutta import RungeKuttaFehlberg54
import numpy as np
import matplotlib.pyplot as plt
import time
import math as m



def F1(Y):
    M = np.array([[-1, -1],
                  [1, -1]])
    res = np.ones(3)
    res[1:3] = M.dot(Y[1:3])
    return res


def EF1(t):
    return m.exp(-t)*m.cos(t), m.exp(-t)*m.sin(t)


def example1(tol, pr):
    W = np.array([0, 1, 0])

    h = 0.25
    tEnd = 1.0
    rkf54 = RungeKuttaFehlberg54(F1, len(W), h, tol)
    accE = 0

    while W[0] < tEnd:
        W, E = rkf54.safeStep(W)
        accE += E

    rkf54.setStepLength(tEnd - W[0])
    W, E = rkf54.step(W)

    if not pr:
        return W,E

    (y1, y2) = W[1:]
    ye1, ye2 = EF1(tEnd)
    print("Funnet: ", y1, y2)
    print("eksakt: ", ye1, ye2)
    print("Globale feil: ", y1 - ye1, y2 - ye2)
    print("Feil fra RFK45: ", E)
    print("Akkumulert feil: ", accE)


example1(1e-14, True)
print("\n")


tol = []
time_y = []
for i in range(15):
    exp = 10**(-(i))
    t0 = time.time()
    example1(exp ,False)
    t1 = time.time()
    tol.append(exp)
    time_y.append(t1-t0)

fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.semilogx(tol, time_y)
ax.axhline(y=10**(-5), color='r')
ax.set_ylabel("Tid (s)")
ax.set_xlabel("Toleranse")
plt.show()

print(tol)