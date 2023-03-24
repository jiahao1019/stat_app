import sys
import numpy as np
import pyqtgraph as pg
 
# Set white background and black foreground
pg.setConfigOption('background', 'k')
pg.setConfigOption('foreground', 'w')
 
# Generate random points
n = 1000
data = np.random.normal(size = (2, n))
 
# Create the main application instance
app = pg.mkQApp()
 
# Create the view
view = pg.PlotWidget()
# view.resize(640, 480)
view.resize(960, 720)
view.setWindowTitle('Scatter plot using pyqtgraph')
view.setAspectLocked(True)
view.show()
 
# Create the scatter plot and add it to the view
pen = pg.mkPen(width = 5, color = 'y')
scatter = pg.ScatterPlotItem(pen = pen, symbol = 'o', size = 2)
view.addItem(scatter)
 
# Convert data array into a list of dictionaries with the x,y-coordinates
# pos = [{'pos': data[:, i]} for i in range(n)]
# scatter.setData(pos) # 2D dictionary
scatter.setData(data[0,:], data[1,:])
 
# execute the application and Gracefully exit the application
sys.exit(app.exec())