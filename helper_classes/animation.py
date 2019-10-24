import time
from opg_4 import *
from opg_5 import *

import numpy as np

import matplotlib.pyplot as plot
import matplotlib.animation as animation
import mpl_toolkits.mplot3d
from mpl_toolkits.mplot3d import axes3d


def circle(pos, size, resolution):
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    x = size * np.outer(np.cos(u), np.sin(v))
    y = size * np.outer(np.sin(u), np.sin(v)) + pos[1]
    z = size * np.outer(np.ones(np.size(u)), np.cos(v)) + pos[0]
    return x, y, z


def animate_two_bodies_3d(orbit, imagescaling, resolution, radius1, radius2, room_size, stepsize=1, steps_per_frame=1,
                          seconds=300, filnavn="orbit", angle=(90, 180), colors=("green", "grey"), movie=True):
    fps = 30
    frames = seconds * fps
    skalering1 = radius1 * imagescaling
    skalering2 = radius2 * imagescaling

    # The figure is set
    fig = plot.figure()
    axes = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim3d=(-room_size, room_size),
                           ylim3d=(-room_size, room_size), zlim3d=(-room_size, room_size), projection='3d')

    # time_text = axes.text(0.02, 0.95, '', transform=axes.transAxes, s='0')
    # energy_text = axes.text(0.02, 0.90, '', transform=axes.transAxes, s='0')

    def animate(i):
        """perform animation step"""
        for i in range(steps_per_frame):
            orbit.step(stepsize)
        axes.clear()
        xs, ys = orbit.position()
        x, y, z = circle([0, 0], skalering1, resolution)
        x1, y1, z1 = circle([xs, ys], skalering2, resolution)
        ball1 = axes.plot_surface(x, y, z, color=colors[0])  # circle(x, y, 10))
        ball2 = axes.plot_surface(x1, y1, z1, color=colors[1])
        axes.set_xlim3d(-room_size, room_size)
        axes.set_ylim3d(-room_size, room_size)
        axes.set_zlim3d(-room_size, room_size)
        axes.view_init(angle[0], angle[1])
        plot.axis('off')
        # time_text = axes.text(0.02, 0.95, '', transform=axes.transAxes, s='0')
        # time_text.set_text('time = %.1f' % orbit.time)
        # energy_text.set_text('energy = %.3f J' % orbit.energy())
        return ball1, ball2  # , time_text #, energy_text

    if not movie:
        animate(0)
        plt.show()
        exit(0)
    # choose the interval based on dt and the time to animate one step
    # Take the time for one call of the animate.

    anim = animation.FuncAnimation(fig,  # figure to plot in
                                   animate,  # function that is called on each frame
                                   frames=frames,  # total number of frames
                                   repeat=False,
                                   blit=True
                                   )

    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    anim.save(filnavn + '.mp4', fps=fps, extra_args=['-vcodec', 'libx264'])
    end_time = time.time()


def graph_satellite_path(orbit, stepsize, time):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ex, ey = [], []
    res = 1000
    for i in range(0, res + 1):
        ex.append((np.cos(i * 2 * np.pi / res)) * radius_earth)
        ey.append((np.sin(i * 2 * np.pi / res)) * radius_earth)
    ax.plot(ex, ey)
    x, y = [], []
    x.append(orbit.satellite.pos_x())
    y.append(orbit.satellite.pos_y())
    for i in range(0, int(time / stepsize)):
        orbit.step(stepsize)
        x.append(orbit.satellite.pos_x())
        y.append(orbit.satellite.pos_y())
    ax.plot(x, y)
    plt.show()


def graph_rocket_path(orbit, stepsize, time):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ex, ey = [], []
    res = 1000
    for i in range(0, res + 1):
        ex.append((np.cos(i * 2 * np.pi / res)) * radius_earth)
        ey.append((np.sin(i * 2 * np.pi / res)) * radius_earth)
    ax.plot(ex, ey)
    mx, my = [], []
    for i in range(0, res + 1):
        mx.append((np.cos(i * 2 * np.pi / res)) * position_moon[0])
        my.append((np.sin(i * 2 * np.pi / res)) * position_moon[0])
    # ax.plot(mx, my)
    x, y = [], []
    x.append(orbit.rocket.pos_x())
    y.append(orbit.rocket.pos_y())
    for i in range(0, int(time / stepsize)):
        orbit.step(stepsize)
        if orbit.rocket.check_crash(radius_earth - 10000) or orbit.rocket.check_too_far(radius_earth):
            print("crash")
            break
        x.append(orbit.rocket.pos_x())
        y.append(orbit.rocket.pos_y())
    ax.plot(x, y)
    plt.show()


def graph_all_rocket_angles(orbit_creator, stepsize, time, interval, intervalstep):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ex, ey = [], []
    res = 1000
    for i in range(0, res + 1):
        ex.append((np.cos(i * 2 * np.pi / res)) * radius_earth)
        ey.append((np.sin(i * 2 * np.pi / res)) * radius_earth)
    ax.plot(ex, ey)
    for a in range(0, int((interval[1] - interval[0]) / intervalstep)):
        angle = interval[0] + intervalstep * a
        print(angle)
        orbit = orbit_creator(angle)
        x, y = [], []
        x.append(orbit.rocket.pos_x())
        y.append(orbit.rocket.pos_y())
        for i in range(0, int(time / stepsize)):
            orbit.step(stepsize)
            if orbit.rocket.check_crash(radius_earth - 1000) or orbit.rocket.check_too_far(radius_earth):
                print("crash")
                break
            x.append(orbit.rocket.pos_x())
            y.append(orbit.rocket.pos_y())
        ax.plot(x, y)

    plt.show()
