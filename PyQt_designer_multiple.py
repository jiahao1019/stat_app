from PyQt6 import QtWidgets, uic
import pyqtgraph as pg
import numpy as np
from scipy.stats import norm
import sys
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        #Load the UI Page by PyQt6
        uic.loadUi('app_0315_multiple.ui', self)
        self.setWindowTitle('A Multi-panel Figure')
        win = self.graphLayoutWidget
         
        self.plt1 = win.addPlot()
        self.plt2 = win.addPlot()
 
        ## generate normal random numbers
        vals = np.hstack([np.random.normal(size=500), np.random.normal(size=260, loc=4)])
 
        ## compute standard histogram
        y, x = np.histogram(vals, bins=np.linspace(-3, 8, 40))
 
        ## Using stepMode="center" causes the plot to draw two lines for each sample.
        ## notice that len(x) == len(y)+1
        self.plt1.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
 
        ## Now draw all points as a nicely-spaced scatter plot
        y = pg.pseudoScatter(vals, spacing=0.15)
        self.plt2.plot(vals, y, pen=None, symbol='o', symbolSize=5, symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
 
        win.nextRow()
        self.plt3 = win.addPlot(title="Parametric, grid enabled")
        self.plt4 = win.addPlot(title="Ellipse")
        x = np.cos(np.linspace(0, 2*np.pi, 1000))
        y = np.sin(np.linspace(0, 4*np.pi, 1000))
        self.plt3.plot(x, y)
        self.plt3.showGrid(x=True, y=True)
 
        p_ellipse = pg.QtGui.QGraphicsEllipseItem(0, 0, 10, 20)  # x, y, width, height
        p_ellipse.setPen(pg.mkPen((0, 0, 0, 100)))
        p_ellipse.setBrush(pg.mkBrush((50, 50, 200)))
        self.plt4.addItem(p_ellipse)
     
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()