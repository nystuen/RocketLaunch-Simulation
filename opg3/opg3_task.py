from rungekutta import *
import time as myTime
import matplotlib.pyplot as plot
import matplotlib.animation as animation
from opg4 import *
from opg5 import *
from opg3.orbit import *

# make an Orbit instance
# init_state: [t0, x0J, vx0J,  y0MJ   vy0J, x0M, vx0M,   y0M,    vy0M],
orbit = Orbit([0, 0, 0, 0, 0, 0, -1022, 384000000, 0],3)

dt = 1. / 30  # 30 frames per second

# The figure is set
fig = plot.figure()
axes = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                       xlim=(-0.5 * 10 ** 9, 0.5 * 10 ** 9), ylim=(-0.5 * 10 ** 9, 0.5 * 10 ** 9))

trail, = axes.plot([], [], 'r--', lw=0.5)
lineA, = axes.plot([], [], 'o-b', lw=60, ms=12)  # A blue planet 6*10**6
lineB, = axes.plot([], [], 'o-r', lw=17, ms=3.4)  # A white planet

# line2, = axes.plot([], [], 'o-y', lw=2)  # A yellow sun
time_text = axes.text(0.02, 0.95, '', transform=axes.transAxes)
energy_text = axes.text(0.02, 0.90, '', transform=axes.transAxes)


def init():
    """initialize animation"""
    lineA.set_data([], [])
    trail.set_data([], [])
    lineB.set_data([], [])
    time_text.set_text('')
    energy_text.set_text('')
    return lineA, lineB, time_text, energy_text


def animate(i):
    """perform animation step"""
    global orbit, dt
    secondsPerFrame = 3600 * 24 / 36
    t0 = orbit.state[0]
    while orbit.state[0] < t0 + secondsPerFrame:
        orbit.step()

    posJ, posM = orbit.position()
    x = posM[0]
    y = posM[1]
    orbit.addPos(x, y)
    trail.set_data(orbit.getPos())
    lineA.set_data(*posJ)
    lineB.set_data(*posM)
    t1 = orbit.time_elapsed()
    antallDager = t1 / (24 * 3600)

    time_text.set_text('time %.3f Days' % antallDager)
    energy_text.set_text('height = %.5f m' % orbit.getValues()[1])
    return lineA, lineB, time_text, energy_text


# choose the interval based on dt and the time to animate one step
# Take the time for one call of the animate.
t0 = myTime.time()
animate(0)
t1 = myTime.time()

delay = 2000 * dt - (t1 - t0)

anim = animation.FuncAnimation(fig,  # figure to plot in
                               animate,  # function that is called on each frame
                               frames=7000,  # total number of frames
                               interval=1.0 / 30,  # time to wait between each frame.
                               repeat=False,
                               blit=True,
                               init_func=init  # initialization
                               )

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
anim.save('Oppg3.html', fps=30, extra_args=['-vcodec', 'libx264'])

#
#
# plot.show()
