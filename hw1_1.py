from PyQt6 import QtWidgets, uic
import pyqtgraph as pg
import numpy as np
from PyQt6.QtWidgets import QMessageBox
from scipy.stats import norm
from scipy.stats import gamma
import sys
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        #Load the UI Page by PyQt6
        uic.loadUi('hw1_1.ui', self)
        self.setWindowTitle('PyQtGraph shows different distribution')
        # self.update_plot('PDF')
        self.pdfcdf_status = 1
        self.update_plot()
        
        # self.pdfcdf_status = 1
        self.label_para1.setText('mu')
        self.label_para2.setText('sigma')
        self.label_UB1.setText('5')
        self.label_LB1.setText('-5')
        self.label_UB2.setText('5')
        self.label_LB2.setText('1')
 
        # Signals
        self.lineEdit_para1.returnPressed.connect(self.update_plot)
        self.lineEdit_para2.returnPressed.connect(self.update_plot)
        self.comboBox.currentIndexChanged.connect(self.set_para)
        self.radioBut_PDF.toggled.connect(self.pdfcdf_clicked)
        self.radioBut_cdf.toggled.connect(self.pdfcdf_clicked)
        self.vSlider_para1.valueChanged.connect(self.sliderMove1)
        self.vSlider_para1.sliderMoved.connect(self.sliderMove1)
        self.vSlider_para2.valueChanged.connect(self.sliderMove2)
        self.vSlider_para2.sliderMoved.connect(self.sliderMove2)
        self.lineEdit_x.returnPressed.connect(self.comp_cdf)
        self.lineEdit_prob.returnPressed.connect(self.comp_invcdf)
        self.pushBtn_exit.clicked.connect(self.dialogBox)


    def update_plot(self):
        # self.gView.clear()
        para1 = int(self.lineEdit_para1.text())
        para2 = int(self.lineEdit_para2.text())
        if self.comboBox.currentText() == 'Normal':
            if (para1 > 5 or para1 < -5) or (para2 > 5 or para2 < 1):
                dlg = QMessageBox(self)
                dlg.setWindowTitle("錯誤")
                dlg.setText("輸入值超過範圍")
                dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
                buttonY = dlg.button(QMessageBox.StandardButton.Yes)
                buttonY.setText('確定')
                dlg.setIcon(QMessageBox.Icon.Question)
                button = dlg.exec()
                self.vSlider_para1.setValue(para1)
                self.vSlider_para2.setValue(para2)
                self.gView.clear()
            else:
                self.vSlider_para1.setValue(para1)
                self.vSlider_para2.setValue(para2)
                x = np.linspace(para1-10, para1+10, 5000)
                if self.pdfcdf_status == 1:
                    y = norm.pdf(x, loc = para1, scale = para2)
                else:
                    y = norm.cdf(x, loc = para1, scale = para2)
                self.gView.clear()
                self.gView.plot(x,y)
        else:
            if (para1 > 11 or para1 < 1) or (para2 > 5 or para2 < 1):
                dlg = QMessageBox(self)
                dlg.setWindowTitle("錯誤")
                dlg.setText("輸入值超過範圍")
                dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
                buttonY = dlg.button(QMessageBox.StandardButton.Yes)
                buttonY.setText('確定')
                dlg.setIcon(QMessageBox.Icon.Question)
                button = dlg.exec()
                self.vSlider_para1.setValue(para1)
                self.vSlider_para2.setValue(para2)
                self.gView.clear()
            else:
                self.vSlider_para1.setValue(para1-6)
                self.vSlider_para2.setValue(para2)
                x = np.linspace(0, 40, 5000)
                if self.pdfcdf_status == 1:
                    y = gamma.pdf(x, a = para1, scale = para2)
                else:
                    y = gamma.cdf(x, a = para1, scale = para2)
                self.gView.clear()
                self.gView.plot(x,y)
    
    def set_para(self):
        if self.comboBox.currentText() == 'Gamma':
            self.gView.clear()
            self.label_para1.setText('alpha')
            self.label_para2.setText('beta')
            self.label_UB1.setText('11')
            self.label_LB1.setText('1')
            self.label_UB2.setText('5')
            self.label_LB2.setText('1')
            self.radioBut_PDF.setChecked(True)
            self.sliderMove1(0)
            self.update_plot()
        else:
            self.gView.clear()
            self.label_para1.setText('mu')
            self.label_para2.setText('sigma')
            self.label_UB1.setText('5')
            self.label_LB1.setText('-5')
            self.label_UB2.setText('5')
            self.label_LB2.setText('1')
            self.radioBut_PDF.setChecked(True)
            self.sliderMove1(0)
            self.update_plot()

    def pdfcdf_clicked(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.pdfcdf_status = -self.pdfcdf_status
            self.update_plot()

    def sliderMove1(self, x):
        if self.comboBox.currentText() == 'Gamma':
            self.lineEdit_para1.setText(str(x+6))
        else:
            self.lineEdit_para1.setText(str(x))
        # print(self.lineEdit_para1.text())

    def sliderMove2(self, y):
        self.lineEdit_para2.setText(str(y))
 
    def comp_cdf(self):
        if self.comboBox.currentText() == 'Normal':
            # print(self.lineEdit_x.displayText())
            cdf = norm.cdf(float(self.lineEdit_x.displayText()), loc = int(self.lineEdit_para1.text()), scale = int(self.lineEdit_para2.text()))    
            self.lineEdit_prob.setText(str(round(cdf, 4)))
            # self.hSlider_x.setValue(int(float(self.lineEdit_x.displayText())))
        else:
            cdf = gamma.cdf(float(self.lineEdit_x.displayText()), a = int(self.lineEdit_para1.text()), scale = int(self.lineEdit_para2.text()))    
            self.lineEdit_prob.setText(str(round(cdf, 4)))

    def comp_invcdf(self):
        if self.comboBox.currentText() == 'Normal':
            x = norm.ppf(float(self.lineEdit_prob.displayText()), loc = int(self.lineEdit_para1.text()), scale = int(self.lineEdit_para2.text()))
            self.lineEdit_x.setText(str(round(x,4)))
        else:
            x = gamma.ppf(float(self.lineEdit_prob.displayText()), a = int(self.lineEdit_para1.text()), scale = int(self.lineEdit_para2.text()))    
            self.lineEdit_x.setText(str(round(x, 4)))

    
    def dialogBox(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Wang's Class Demo")
        dlg.setText("確定要離開這個 App")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        buttonY = dlg.button(QMessageBox.StandardButton.Yes)
        buttonY.setText('確定')
        buttonY = dlg.button(QMessageBox.StandardButton.No)
        buttonY.setText('取消')
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()
 
        if button == QMessageBox.StandardButton.Yes:
            self.close()
        else:
            print("No!")


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()