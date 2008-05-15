from pylab import *
import numpy.random as random

ion()
ax = subplot(111)
data = random.normal(5, 2, (1000, 2))
dots, = ax.plot(data[:,0], data[:,1], '.', ms=1)

hline = ax.axhline(5, c='r', animated=True)
vline = ax.axvline(5, c='r')

# xmin, xmax, ymin, ymax = ax.axis()
# lines = []
# lines.append(dots)
# line, = ax.plot([0, 10], [0, 10], 'r-') 
# lines.append(line)
# line, = ax.plot([0, 10], [0, 10], 'r-') 
# lines.append(line)

# lines = [dots, hline, vline]

def on_move(event):
    # get the x and y pixel coords
    x, y = event.x, event.y

    if event.inaxes:
        print 'data coords', event.xdata, event.ydata

def on_click(event):
    x, y = event.x, event.y

    if event.inaxes and event.button==1:
        print 'data coords', event.xdata, event.ydata

    # line, = ax.plot([event.ydata, event.ydata], [ymin, ymax], 'r-')
    # lines[1].set_data(line)

    # line, = ax.plot([xmin, xmax], [event.xdata, event.xdata], 'r-')
    # lines[2].set_data(line)

    lines[1] = axhline(event.ydata, c='r')
    lines[2] = axvline(event.xdata, c='r')

    draw()

# connect('motion_notify_event', on_move)
connect('button_press_event', on_click)

raw_input()

# show()

# show()
