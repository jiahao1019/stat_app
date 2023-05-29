from PyQt6 import QtWidgets, uic, QtGui, QtCore
from PyQt6.QtWidgets import QMessageBox
import matplotlib.image as mpimg
from PyQt6.QtCore import Qt
import pyqtgraph as pg
from scipy.stats import norm
from scipy.stats import gamma
import pandas as pd
import numpy as np
from pathlib import Path
import sys, os, chardet

class TableModel(QtCore.QAbstractTableModel):
 
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
 
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
 
        if role == Qt.ItemDataRole.TextAlignmentRole:          
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignHCenter
         
        if role == Qt.ItemDataRole.BackgroundRole and (index.row()%2 == 0):
            return QtGui.QColor('#C5C9C7')
 
    def rowCount(self, index):
        return self._data.shape[0]
 
    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
 
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('711033107_hw1.ui', self)
        self.tabWidget.setCurrentIndex(0)
        self.setWindowTitle('3 Apps on one window')
        self.tabpage = 0
        self.tabWidget.currentChanged.connect(self.tabChange)

    # Page1 default
        self.s = 1
        self.img_dir = ''
    
    # Page1 Signals
        self.pBut_first.clicked.connect(self.showImg1)
        self.pBut_previous.clicked.connect(self.showImg2)
        self.pBut_next.clicked.connect(self.showImg3)
        self.pBut_last.clicked.connect(self.showImg4)
        self.actionOpen_1.triggered.connect(self.folderOpen)

    # Page2 default
        self.pdfcdf_status = 1
        self.update_plot()
        self.label_para1.setText('mu')
        self.label_para2.setText('sigma')
        self.label_UB1.setText('5')
        self.label_LB1.setText('-5')
        self.label_UB2.setText('5')
        self.label_LB2.setText('1')
 
    # Page2 Signals
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
        self.gView.scene().sigMouseMoved.connect(self.mouseMoved)
        self.gView.scene().sigMouseClicked.connect(self.mouse_clicked)

    # Page3 default
        self.table = self.tableView
        win = self.graphLayoutWidget
        self.plt1 = win.addPlot(title="")
        win.nextRow()
        self.plt2 = win.addPlot(title="")
 
    # Page3 Signals
        self.actionExit_1.triggered.connect(self.fileExit)
        self.actionOpen_1.triggered.connect(self.fileOpen)
        self.cBox_col.currentIndexChanged.connect(self.plot1)
        self.cBox_scatter_row.currentIndexChanged.connect(self.plot2)
        self.cBox_scatter_col.currentIndexChanged.connect(self.plot2)
    
    def tabChange(self):
        self.tabpage = self.tabWidget.currentIndex()

    # Page1 Slot
    def showImg1(self):
        self.graphWidget.clear()
        image = mpimg.imread(self.img_dir + '/' + os.listdir(self.img_dir)[0])
        img_item = pg.ImageItem(image, axisOrder='row-major')
        self.graphWidget.addItem(img_item)
        self.graphWidget.invertY(True)
        self.graphWidget.getAxis('bottom').setTicks('')
        self.graphWidget.getAxis('left').setTicks('')
        self.graphWidget.setAspectLocked(lock=True, ratio=1)
        self.label_cap.setText('第 1 頁')
        self.s = 1

    def showImg2(self):
        if self.s > 1:
            self.s -= 1
            self.graphWidget.clear()
            image = mpimg.imread(self.img_dir + '/' + os.listdir(self.img_dir)[self.s-1])
            img_item = pg.ImageItem(image, axisOrder='row-major')
            self.graphWidget.addItem(img_item)
            self.graphWidget.invertY(True)
            self.graphWidget.getAxis('bottom').setTicks('')
            self.graphWidget.getAxis('left').setTicks('')
            self.graphWidget.setAspectLocked(lock=True, ratio=1)
            self.label_cap.setText(f'第 {self.s} 頁')
        else:
            self.graphWidget.clear()
            image = mpimg.imread(self.img_dir + '/' + os.listdir(self.img_dir)[0])
            img_item = pg.ImageItem(image, axisOrder='row-major')
            self.graphWidget.addItem(img_item)
            self.graphWidget.invertY(True)
            self.graphWidget.getAxis('bottom').setTicks('')
            self.graphWidget.getAxis('left').setTicks('')
            self.graphWidget.setAspectLocked(lock=True, ratio=1)
            self.label_cap.setText(f'第 {1} 頁')
            self.s = 1

    def showImg3(self):
        if self.s < len(os.listdir(self.img_dir)):
            self.s += 1
            self.graphWidget.clear()
            image = mpimg.imread(self.img_dir + '/' + os.listdir(self.img_dir)[self.s-1])
            img_item = pg.ImageItem(image, axisOrder='row-major')
            self.graphWidget.addItem(img_item)
            self.graphWidget.invertY(True)
            self.graphWidget.getAxis('bottom').setTicks('')
            self.graphWidget.getAxis('left').setTicks('')
            self.graphWidget.setAspectLocked(lock=True, ratio=1)
            self.label_cap.setText(f'第 {self.s} 頁')
        else:
            self.graphWidget.clear()
            image = mpimg.imread(self.img_dir + '/' + os.listdir(self.img_dir)[len(os.listdir(self.img_dir))-1])
            img_item = pg.ImageItem(image, axisOrder='row-major')
            self.graphWidget.addItem(img_item)
            self.graphWidget.invertY(True)
            self.graphWidget.getAxis('bottom').setTicks('')
            self.graphWidget.getAxis('left').setTicks('')
            self.graphWidget.setAspectLocked(lock=True, ratio=1)
            self.label_cap.setText(f'第 {len(os.listdir(self.img_dir))} 頁')
            self.s = len(os.listdir(self.img_dir))

    def showImg4(self):
        self.graphWidget.clear()
        image = mpimg.imread(self.img_dir + '/' + os.listdir(self.img_dir)[len(os.listdir(self.img_dir))-1])
        img_item = pg.ImageItem(image, axisOrder='row-major')
        self.graphWidget.addItem(img_item)
        self.graphWidget.invertY(True)
        self.graphWidget.getAxis('bottom').setTicks('')
        self.graphWidget.getAxis('left').setTicks('')
        self.graphWidget.setAspectLocked(lock=True, ratio=1)
        self.label_cap.setText(f'第 {len(os.listdir(self.img_dir))} 頁')
        self.s = len(os.listdir(self.img_dir))

    def folderOpen(self):
        if self.tabpage == 0:
            folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Open folder", "./")
            self.image = mpimg.imread(folder_path + '/' + os.listdir(folder_path)[0])
            self.img_item = pg.ImageItem(self.image, axisOrder='row-major')
            self.graphWidget.addItem(self.img_item)
            self.graphWidget.invertY(True)
            self.graphWidget.getAxis('bottom').setTicks('')
            self.graphWidget.getAxis('left').setTicks('')
            self.graphWidget.setAspectLocked(lock=True, ratio=1)
            self.label_open.setHidden(True)
            self.img_dir = folder_path
        else:
            pass

    def fileExit(self):
        self.close()
    
    # Page2 Slot
    def update_plot(self):
        self.gView.clear()
        para1 = float(self.lineEdit_para1.text())
        para2 = float(self.lineEdit_para2.text())
        if self.comboBox.currentText() == 'Normal':
            if (para1 > 5 or para1 < -5) or (para2 > 5 or para2 < 1):
                dlg = QMessageBox()
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
                self.vLine = pg.InfiniteLine(pos = 1, angle=90, movable=False)
                self.hLine = pg.InfiniteLine(pos = 0.2, angle=0, movable=False)
                self.gView.addItem(self.vLine)
                self.gView.addItem(self.hLine)
        else:
            if (para1 > 11 or para1 < 1) or (para2 > 5 or para2 < 1):
                dlg = QMessageBox()
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
                self.vLine = pg.InfiniteLine(pos = 1, angle=90, movable=False)
                self.hLine = pg.InfiniteLine(pos = 0.2, angle=0, movable=False)
                self.gView.addItem(self.vLine)
                self.gView.addItem(self.hLine)
    
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
        self.update_plot()

    def sliderMove2(self, y):
        self.lineEdit_para2.setText(str(y))
        self.update_plot()
 
    def comp_cdf(self):
        if self.comboBox.currentText() == 'Normal':
            cdf = norm.cdf(float(self.lineEdit_x.displayText()), loc = int(self.lineEdit_para1.text()), scale = int(self.lineEdit_para2.text()))    
            self.lineEdit_prob.setText(str(round(cdf, 4)))
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
    
    def mouseMoved(self, point):
        p = self.gView.plotItem.vb.mapSceneToView(point)
        self.vLine.setPos(p.x())
        self.hLine.setPos(p.y())

    def mouse_clicked(self, evt):
        vb = self.gView.plotItem.vb
        scene_coords = evt.scenePos()
        if self.gView.sceneBoundingRect().contains(scene_coords):
            mouse_point = vb.mapSceneToView(scene_coords)
            self.lineEdit_x.setText(str(round(mouse_point.x(), 4))) 
            self.lineEdit_prob.setText(str(round(norm.cdf(mouse_point.x()), 4)))
   
    def dialogBox(self):
        dlg = QMessageBox()
        dlg.setWindowTitle("離開程式")
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

    # Page3 Slot
    def fileOpen(self):
        if self.tabpage == 2:
            home_dir = str(Path.home())
            fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', "", "EXCEL files (*.xlsx *.xls);;CSV (*.csv)")
            if ('xlsx' or 'xls') in fname[0]:
                self.df = pd.read_excel(fname[0], index_col = None, header = 0)
                self.model = TableModel(self.df)
                self.table.setModel(self.model)
    
                self.label_variable.setText(str(self.df.shape[1]))
                self.label_size.setText(str(self.df.shape[0]))
                self.cBox_col.clear()
                self.cBox_col.addItems(self.df.columns)
                self.cBox_scatter_row.addItems(self.df.columns)
                self.cBox_scatter_col.addItems(self.df.columns)
            else:
                with open(fname[0], 'rb') as f:
                    tmp = chardet.detect(f.read())   # 取得CSV檔的encoding
                self.df = pd.read_csv(fname[0], index_col = None, header = 0, encoding = tmp['encoding'])
                self.model = TableModel(self.df)
                self.table.setModel(self.model)
    
                self.label_variable.setText(str(self.df.shape[1]))
                self.label_size.setText(str(self.df.shape[0]))
                self.cBox_col.clear()
                self.cBox_col.addItems(self.df.columns)
                self.cBox_scatter_row.addItems(self.df.columns)
                self.cBox_scatter_col.addItems(self.df.columns)
        else:
            pass

    def plot1(self):
        self.plt1.clear()
        y, x = np.histogram(self.df[self.cBox_col.currentText()])
        barItem = pg.BarGraphItem(x = x[0:len(y)-1], height = y, width = (x.max()-x.min())/len(x), brush=(107,200,224))
        self.plt1.addItem(barItem)
        self.plt1.setTitle(self.cBox_col.currentText())

    def plot2(self):
        if self.cBox_scatter_col.currentText() != '':
            self.plt2.clear()
            if isinstance(self.df[self.cBox_scatter_row.currentText()][0], str) or isinstance(self.df[self.cBox_scatter_col.currentText()][0], str) :
                self.plt2.setLabel('bottom','')   
                self.plt2.setLabel('left','')
                return
            else:
                self.plt2.plot(self.df[self.cBox_scatter_row.currentText()], self.df[self.cBox_scatter_col.currentText()], 
                            pen = None, symbol = 'o', symbolSize = 5)
                self.plt2.setLabel('bottom',self.cBox_scatter_row.currentText())
                self.plt2.setLabel('left',self.cBox_scatter_col.currentText())
        else:
            self.plt2.clear()
      
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()