import sys
import numpy as np
from scipy.stats import norm
import pyqtgraph as pg
 
plt = pg.plot()
plt.setWindowTitle('FillBetweenItem')
plt.setYRange(0, 0.5)
 
x = np.linspace(-5, 5, 1000)
y = norm.pdf(x)
 
pen = pg.mkPen(color=(255, 0, 0), width = 10) # linestyle=Qt.DotLine, Qt.DashDotLine and Qt.DashDotDotLine    
cur = plt.plot(x, y, pen = pen)
 
x = np.linspace(-1.96, 1.96, 200)
y = norm.pdf(x)
cur1 = plt.plot(x, y, pen = 'r', name = 'Demo')
cur2 = plt.plot(x, np.zeros(len(y)))
        # add color patch under curve
patchcur = pg.FillBetweenItem(curve1 = cur1, curve2 = cur2, \
    brush = 'green')
plt.addItem(patchcur)
 
# x = np.linspace(-2.576, 2.576, 200)
# y = norm.pdf(x)
# cur1.setData(x, y)
# cur2.setData(x, np.zeros(len(y)))
 
if __name__ == '__main__':
    sys.exit(pg.exec())
