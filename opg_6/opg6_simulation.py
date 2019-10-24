# for Python2
# from tkinter import *   ## notice capitalized T in Tkinter
from helper_classes.orbit import *
import time as myTime
import numpy as np
# for Python2
# from tkinter import *   ## notice capitalized T in Tkinter
import matplotlib.pyplot as plot
import matplotlib.animation as animation

# make an Orbit instance
# init_state: [t0, x0J, vx0J,  y0MJ   vy0J, x0R, vx0R,   y0R,    vy0R],
orbit = Orbit([0, 0, 0, 0, 0.1, 1, 0.1, 6371000, 0.1], 6)
dt = 1. / 120  # 30 frames per second

# The figure is set
fig = plot.figure()
axes = fig.add_subplot(111, aspect='auto', autoscale_on=False,
                       xlim=(-(2 * 6371000), 2 * 6371000), ylim=(-(2 * 6371000), 2 * 6371000))

axes.set_facecolor('xkcd:white')
# axes.set_facecolor((1.0, 0.47, 0.42))
trail, = axes.plot([], [], 'r--', lw=0.5)
lineA, = axes.plot([], [], 'o-b', lw=60, ms=128)  # A blue planet 6*10**6
lineB, = axes.plot([], [], 'o-r', lw=17, ms=3.4)  # A white planet

# line2, = axes.plot([], [], 'o-y', lw=2)  # A yellow sun
time_text = axes.text(0.02, 0.95, '', transform=axes.transAxes)
height_text = axes.text(0.02, 0.90, '', transform=axes.transAxes)
speed_text = axes.text(0.02, 0.85, '', transform=axes.transAxes)
params = {"ytick.color": "w",
          "xtick.color": "w",
          "axes.labelcolor": "w",
          "axes.edgecolor": "w"}
plot.rcParams.update(params)


def init():
    """initialize animation"""
    lineA.set_data([], [])
    trail.set_data([], [])
    lineB.set_data([], [])
    time_text.set_text('')
    speed_text.set_text('')
    return lineA, lineB, time_text


def animate(i):
    """perform animation step"""
    global orbit, dt
    secondsPerFrame = 90
    t0 = orbit.state[0]
    while orbit.state[0] < t0 + secondsPerFrame:
        orbit.step()
    posJ, posR = orbit.position()
    x = posR[0]
    y = posR[1]
    height = (np.sqrt(posR[1] ** 2 + posR[0] ** 2) - radius_earth) / 1000
    if height < 0:
        raise ValueError('Rocket crashed, exiting')
        exit - 1
    orbit.addPos(x, y)
    trail.set_data(orbit.getPos())
    lineA.set_data(*posJ)
    lineB.set_data(*posR)
    t1 = orbit.time_elapsed()

    speed_text.set_text('Speed: %.3f' % orbit.getValues()[0])
    time_text.set_text('Time: %.3f ' % t1)
    height_text.set_text('Height: %.3f km' % height)

    return lineA, lineB, time_text, height_text, speed_text


# choose the interval based on dt and the time to animate one step
# Take the time for one call of the animate.
t0 = myTime.time()
animate(0)
t1 = myTime.time()

delay = 2000 * dt - (t1 - t0)

anim = animation.FuncAnimation(fig,  # figure to plot in
                               animate,  # function that is called on each frame
                               frames=1000,  # total number of frames
                               interval=delay,  # time to wait between each frame.
                               repeat=False,
                               blit=True,
                               init_func=init  # initialization
                               )

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
anim.save('Oppgave6.html', fps=3000, extra_args=['-vcodec', 'libx264'])

# plot.show()
