import numpy as np
from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui

title = "Basic pyqtgraph plot"

x = range(0, 10)
y1 = [2, 8, 6, 8, 6, 11, 14, 13, 18, 19]
y2 = [3, 1, 5, 8, 9, 11, 16, 17, 14, 16]

plt = pg.plot()

plt.showGrid(x = True, y = True)
plt.addLegend(offset = (150,5),labelTextSize = "16pt")
plt.setLabel('left', 'y')
plt.setLabel('bottom', 'x')
plt.setWindowTitle(title)


line1 = plt.plot(x, y1, pen ='g', symbol ='x', \
    symbolPen ='g', symbolBrush = 0.2, name ='green')
  
line2 = plt.plot(x, y2, pen ='y', symbol ='o', \
    symbolPen ='y', symbolBrush = 0.2, name ='blue')

# main method
if __name__ == '__main__':
      
    # Create the main application instance
    # QtGui.QApplication.instance().exec()
    import sys
    # app = QtGui.QApplication.instance()
    app = QtWidgets.QApplication.instance()
    sys.exit(app.exec())