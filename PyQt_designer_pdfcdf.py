from PyQt6 import QtWidgets, uic
import pyqtgraph as pg
import numpy as np
from scipy.stats import norm
import sys
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        #Load the UI Page by PyQt6
        uic.loadUi('app_0315_1.ui', self)
        self.setWindowTitle('PyQtGraph shows normal distribution')
        self.pdfcdf_status = 1
 
        # Signals
        self.pdfcdf.clicked.connect(self.update_plot)
        self.checkBox_Grid.stateChanged.connect(self.gridon)
        self.lineEdit_x.returnPressed.connect(self.comp_cdf)
        self.lineEdit_cdfx.returnPressed.connect(self.comp_invcdf)
        self.hSlider_x.valueChanged.connect(self.sliderMove)
        self.hSlider_x.sliderMoved.connect(self.sliderMove)
        self.update_plot()
         
    # Slots
    def update_plot(self):
        self.graphWidget.clear() # clear current plot before plotting
        x = np.linspace(-5, 5, 1000)
        if self.pdfcdf_status == 1:
            y = norm.pdf(x)
            titlename = "PDF"
        else:
            y = norm.cdf(x)
            titlename = "CDF"
        pen = pg.mkPen(color=(255, 0, 0), width = 10) # Qt.DotLine, Qt.DashDotLine and Qt.DashDotDotLine
     
        cur1 = self.graphWidget.plot(x, y, pen = pen, name = 'Demo')
        cur2 = self.graphWidget.plot(x, np.zeros(len(y)))
        # add color patch under curve
        patchcur = pg.FillBetweenItem(curve1 = cur1, curve2 = cur2, brush = 'g')
        if self.pdfcdf_status == 1:
            self.graphWidget.addItem(patchcur)
         
        self.graphWidget.setBackground('w')
        self.graphWidget.setTitle(titlename, color="b", size="14pt")
        styles = {'color':'green', 'font-size':'16px'}
        self.graphWidget.setLabel('left', 'Y', **styles)
        self.graphWidget.setLabel('bottom', 'X', **styles)
        self.graphWidget.showGrid(x=False, y=False)
        self.pdfcdf_status = -self.pdfcdf_status
 
    def gridon(self, s):
        # print(self.checkBox_Grid.checkState())
        if s == 2: # 0 : unchecked; 2 : checked
            self.graphWidget.showGrid(x = True, y = True)   
        else:
            self.graphWidget.showGrid(x = False, y = False)
        # print(s)
 
    def comp_cdf(self):
        # print(self.lineEdit_x.displayText())
        cdf = norm.cdf(float(self.lineEdit_x.displayText()))    
        self.lineEdit_cdfx.setText(str(round(cdf, 4)))
        self.hSlider_x.setValue(int(float(self.lineEdit_x.displayText())))

    def comp_invcdf(self):
        x = norm.ppf(float(self.lineEdit_cdfx.displayText()))
        self.lineEdit_x.setText(str(round(x,4)))

    def sliderMove(self, x):
        self.lineEdit_x.setText(str(round(x,4)))
        self.lineEdit_cdfx.setText(str(round(norm.cdf(x), 4)))

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()