import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt
import chardet
import pyqtgraph as pg
import pandas as pd
import numpy as np
from pathlib import Path
 
 
class TableModel(QtCore.QAbstractTableModel):
 
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
 
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()] #pandas's iloc method
            return str(value)
 
        if role == Qt.ItemDataRole.TextAlignmentRole:          
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignHCenter
         
        if role == Qt.ItemDataRole.BackgroundRole and (index.row()%2 == 0):
            return QtGui.QColor('#d8ffdb')
 
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
 
    def __init__(self):
        super().__init__()
 
        uic.loadUi('PyQtTable_pandas.ui', self)
        self.setWindowTitle('Table View: the pandas version')
        self.table = self.tableView
        win = self.graphLayoutWidget
        self.plt1 = win.addPlot(title="")
        win.nextRow()
        self.plt2 = win.addPlot(title="")
 
        #Signals
        self.actionExit.triggered.connect(self.fileExit)
        self.actionOpen.triggered.connect(self.fileOpen)
        self.cBox_col.currentIndexChanged.connect(self.plot1)
        self.cBox_scatter_row.currentIndexChanged.connect(self.plot2)
        self.cBox_scatter_col.currentIndexChanged.connect(self.plot2)
 
    # Slots:
    def fileExit(self):
        self.close()
 
    def fileOpen(self):
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

    def plot1(self):
        self.plt1.clear()
        y, x = np.histogram(self.df[self.cBox_col.currentText()])
        barItem = pg.BarGraphItem(x = x[0:len(y)-1], height = y, width = (x.max()-x.min())/len(x), brush=(107,200,224))
        self.plt1.addItem(barItem)
        self.plt1.setTitle(self.cBox_col.currentText())

    def plot2(self):
        if self.cBox_scatter_col.currentText() != '':
            self.plt2.clear()
            print(self.cBox_scatter_row.currentText())
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