import sys
import numpy as np
import pyqtgraph as pg

app = pg.mkQApp()

win = pg.GraphicsLayoutWidget(show = True, title = "Basic plotting examples")
plt1 = win.addPlot(title = "n = 10")
plt2 = win.addPlot(title = "n = 100")

vals = np.random.normal(size = 10)
y, x = np.histogram(vals, bins = np.linspace(-3, 3, 10))
plt1.plot(x, y, stepMode = "center", fillLevel = 0, fillOutline = True, brush = (0,0,255,150))

vals = np.random.normal(size = 100)
y, x = np.histogram(vals, bins = np.linspace(-3, 3, 10))
plt2.plot(x, y, stepMode = "center", fillLevel = 0, fillOutline = True, brush = (0,0,255,150))

win.nextRow()
plt3 = win.addPlot(title = "n = 1000")
plt4 = win.addPlot(title = "n = 10000")

vals = np.random.normal(size = 1000)
y, x = np.histogram(vals, bins = np.linspace(-3, 3, 100))
plt3.plot(x, y, stepMode = "center", fillLevel = 0, fillOutline = True, brush = (0,0,255,150))

vals = np.random.normal(size = 100000)
y, x = np.histogram(vals, bins = np.linspace(-3, 3, 500))
plt4.plot(x, y, stepMode = "center", fillLevel = 0, fillOutline = True, brush = (0,0,255,150))

sys.exit(app.exec())