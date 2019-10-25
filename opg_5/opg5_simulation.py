# for Python2
# from tkinter import *   ## notice capitalized T in Tkinter
from helper_classes.orbit import *
import time as myTime
import matplotlib.pyplot as plot
import matplotlib.animation as animation

# make an Orbit instance
# init_state: [t0, x0J, vx0J,  y0MJ   vy0J, x0R, vx0R,   y0R,    vy0R],
orbit = Orbit([0, 0, 0, 0, 0, 0, 0, 6371000, 0], 5)
dt = 1. / 30  # 30 frames per second

fig = plot.figure()
axes = fig.add_subplot(111, aspect='auto', autoscale_on=False,
                       xlim=(-30000, 30000), ylim=(6371000, 6371000 + 1210000))

trail, = axes.plot([], [], 'r--', lw=0.5)
lineA, = axes.plot([], [], 'o-b', lw=60, ms=12)  # A blue planet 6*10**6
lineB, = axes.plot([], [], 'o-r', lw=17, ms=3.4)  # A white planet

# line2, = axes.plot([], [], 'o-y', lw=2)  # A yellow sun
time_text = axes.text(0.02, 0.95, '', transform=axes.transAxes)
height_text = axes.text(0.02, 0.90, '', transform=axes.transAxes)
speed_text = axes.text(0.02, 0.85, '', transform=axes.transAxes)


maxHeight = 0
currentHeight = 0
timeAtMaxHeight = 0

maxSpeed = 0
currentSpeed = 0
timeAtMaxSpeed = 0

def init():
    lineA.set_data([], [])
    trail.set_data([], [])
    lineB.set_data([], [])
    time_text.set_text('')
    speed_text.set_text('')
    return lineA, lineB, time_text, speed_text




def animate(i):
    global orbit, dt, maxHeight, maxSpeed, timeAtMaxHeight, timeAtMaxSpeed
    secondsPerFrame = 0.3
    t0 = orbit.state[0]
    while orbit.state[0] < t0 + secondsPerFrame:
        orbit.step()
    posJ, posR = orbit.position()
    x = posR[0]
    y = posR[1]
    height = (posR[1] - 6371010) / 1000
    orbit.addPos(x, y)
    lineA.set_data(*posJ)
    lineB.set_data(*posR)
    t1 = orbit.time_elapsed()

    currentSpeed =  orbit.getValues()[0]
    currentHeight = height


    if(currentHeight > maxHeight):
        maxHeight = currentHeight
        timeAtMaxHeight = t1
    if(currentSpeed > maxSpeed):
        maxSpeed = currentSpeed
        timeAtMaxSpeed = t1



    speed_text.set_text('Speed: %.3f' % currentSpeed)
    time_text.set_text('Time %.3f S' % t1)
    height_text.set_text('Height = %.5f km' % currentHeight)

    return lineA, lineB, time_text, speed_text


# Choose the interval based on dt and the time to animate one step, take the time for one call of the animate.
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


print('Max height:', maxHeight,'. Time:', timeAtMaxHeight)
print('Max speed:', maxSpeed,'. Time:', timeAtMaxSpeed)


anim.save('Oppgave5.html', fps=30, extra_args=['-vcodec', 'libx264'])
