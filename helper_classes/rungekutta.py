#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 20:26:05 2018

@author: rivertz
"""

import numpy as np
import math as m
import sys
import time
import matplotlib.pyplot as plt


class RungeKuttaFehlberg54:
    A = np.array(
        [[0, 0, 0, 0, 0, 0],
         [1 / 4, 0, 0, 0, 0, 0],
         [3 / 32, 9 / 32, 0, 0, 0, 0],
         [1932 / 2197, -7200 / 2197, 7296 / 2197, 0, 0, 0],
         [439 / 216, -8, 3680 / 513, -845 / 4104, 0, 0],
         [-8 / 27, 2, -3544 / 2565, 1859 / 4104, -11 / 40, 0]])

    B = np.array(
        [[25 / 216, 0, 1408 / 2565, 2197 / 4104, -1 / 5, 0],
         [16 / 135, 0, 6656 / 12825, 28561 / 56430, -9 / 50, 2 / 55]]);

    def __init__(self,
                 function,
                 dimension,
                 stepsize,
                 tolerance):
        self.F = function;
        self.dim = dimension;
        self.h = stepsize;
        self.tol = tolerance;

    def step(self,
             Win):
        s = np.zeros((6, self.dim))

        for i in range(0, 6):
            s[i, :] = self.F(Win + self.h * self.A[i, 0:i].dot(s[0:i, :]))

        Zout = Win + self.h * (self.B[0, :].dot(s));
        Wout = Win + self.h * (self.B[1, :].dot(s));

        E = np.linalg.norm(Wout - Zout, 2) / np.linalg.norm(Wout, 2);
        return Wout, E

    def safeStep(self,
                 Win):
        Wout, E = self.step(Win);
        # Check if the error is tolerable
        if (not self.isErrorTolerated(E)):
            # Try to adjust the optimal step length
            self.adjustStep(E);
            Wout, E = self.step(Win);
        # If the error is still not tolerable
        counter = 0;
        while (not self.isErrorTolerated(E)):
            # Try if dividing the steplength with 2 helps.
            self.divideStepByTwo();
            Wout, E = self.step(Win);
            counter = counter + 1;
            if (counter > 10):
                sys.exit(-1);

        self.adjustStep(E);

        return Wout, E

    def isErrorTolerated(self, E):
        return E < self.tol;

    def adjustStep(self, E):
        if (E == 0):
            s = 2;
        else:
            s = m.pow(self.tol * self.h / (2 * E), 0.25);
        self.h = s * self.h;

    def divideStepByTwo(self):
        self.h = self.h / 2;

    def setStepLength(self, stepLength):
        self.h = stepLength;


def F(Y):
    M = np.array([[0.49119653, 0.32513304, 0.98057799],
                  [0.20768544, 0.97699416, 0.18220559],
                  [0.96407071, 0.18373237, 0.95307793]]);
    res = np.ones(4);
    res[1:4] = M.dot(Y[1:4]);
    return res;


def F1(Y):
    M = np.array([[-1, -1],
                  [1, -1]])
    res = np.ones(3)
    res[1:3] = M.dot(Y[1:3])
    return res


def EF1(t):
    return m.exp(-t) * m.cos(t), m.exp(-t) * m.sin(t)


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
        return W, E

    (y1, y2) = W[1:]
    ye1, ye2 = EF1(tEnd)
    print("funnet: ", y1, y2)
    print("eksakt: ", ye1, ye2)
    print("Globale feil: ", y1 - ye1, y2 - ye2)
    print("Feil fra RFK45: ", E)
    print("Akkumulert feil: ", accE)


example1(1e-14, True)
print("\n")

tol = []
time_y = []
for i in range(15):
    exp = 10 ** (-(i))
    t0 = time.time()
    example1(exp, False)
    t1 = time.time()
    tol.append(exp)
    time_y.append(t1 - t0)

fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.semilogx(tol, time_y)
ax.axhline(y=10 ** (-5), color='r')
ax.set_ylabel("Tid (s)")
ax.set_xlabel("Toleranse")
plt.show()

print(tol)