import sys
import numpy as np
import pyqtgraph as pg
 
# Create the main application instance
app = pg.mkQApp()

# Create the view
win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
plt1 = win.addPlot()
plt2 = win.addPlot()

# make interesting distribution of values
vals = np.hstack([np.random.normal(size=500), np.random.normal(size=260, loc=4)])
# compute standard histogram
y, x = np.histogram(vals, bins=np.linspace(-3, 8, 40))
# Using stepMode="center" causes the plot to draw two lines for each sample.
# notice that len(x) == len(y)+1
plt1.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
# Now draw all points as a nicely-spaced scatter plot
y = pg.pseudoScatter(vals, spacing=0.15)
plt2.plot(vals, y, pen=None, symbol='o', symbolSize=5, symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))

win.nextRow()
plt3 = win.addPlot(title="Parametric, grid enabled")
plt4 = win.addPlot(title="Ellipse")

x = np.cos(np.linspace(0, 2*np.pi, 1000))
y = np.sin(np.linspace(0, 4*np.pi, 1000))
plt3.plot(x, y)
plt3.showGrid(x=True, y=True)

p_ellipse = pg.QtGui.QGraphicsEllipseItem(0, 0, 10, 20)  # x, y, width, height
p_ellipse.setPen(pg.mkPen((0, 0, 0, 100)))
p_ellipse.setBrush(pg.mkBrush((50, 50, 200)))
plt4.addItem(p_ellipse)

# execute the application and Gracefully exit the application
sys.exit(app.exec())