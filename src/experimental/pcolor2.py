import numpy
import pylab

xn1 = numpy.random.normal(0, 0.63, 10000)
yn1 = numpy.random.normal(0, 0.63, 10000)

xn2 = numpy.random.normal(0.5, 0.23, 15000)
yn2 = numpy.random.normal(0.5, 0.23, 15000)

xu = numpy.random.uniform(-5, 5, 1000)
yu = numpy.random.uniform(-5, 5, 1000)

x = numpy.concatenate([xn1, xn2, xu])
y = numpy.concatenate([yn1, yn2, yu])

bins = 250
z, xedge, yedge = numpy.histogram2d(y, x, bins=[bins, bins], 
                                    range=[(numpy.min(y), numpy.max(y)),
                                           (numpy.min(x), numpy.max(x))])

xint = map(int, (x - numpy.min(x))/(numpy.max(x)-numpy.min(x))*(bins-1))
yint = map(int, (y - numpy.min(y))/(numpy.max(y)-numpy.min(y))*(bins-1))

zvals = numpy.array([z[_y, _x] for _x, _y in zip(xint, yint)])

print max(xint), max(yint)

ax = pylab.subplot(111)
ax.scatter(x, y, s=1, c=zvals, faceted=False)

# ax.contour(numpy.linspace(-3, 3, num=150), numpy.linspace(-3, 3, num=150), z)
ax.set_xlabel('X')
ax.set_ylabel('Y')
pylab.show()
