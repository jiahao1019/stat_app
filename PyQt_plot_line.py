import numpy as np
from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui # 這個宣告會引用 PyQt 的 QtGui, QtCore
 
# define the data
title = "Basic pyqtgraph plot"

x = np.linspace(-3*np.pi, 3*np.pi, 1000)
y1 = np.sin(x)
y2 = np.cos(x)
y = y1 + y2
 
# create plot window object
plt = pg.plot()
 
# some regular settings
plt.showGrid(x = True, y = True)
plt.addLegend(offset = (150,5),labelTextSize = "16pt")
plt.setLabel('left', 'y') # <font>&mu;</font>
plt.setLabel('bottom', 'x') # <math>sin(x)
# plt.setXRange(0, 10)
plt.setYRange(-2.5, 2.5)
plt.setWindowTitle(title)
 
plt.plot(x, y1, pen = 'g', name = 'sin(x)')
plt.plot(x, y2, pen = 'r', name = 'cos(x)')
 
pen = pg.mkPen(color='y', width=3, style = QtCore.Qt.PenStyle.DashLine) # style = QtCore.Qt.DotLine
plt.plot(x, y, pen = pen, name = 'sin(x)+cos(x)')
 
# main method
if __name__ == '__main__':
      
    # Create the main application instance
    # QtGui.QApplication.instance().exec()
    import sys
    # app = QtGui.QApplication.instance()
    app = QtWidgets.QApplication.instance()
    sys.exit(app.exec())