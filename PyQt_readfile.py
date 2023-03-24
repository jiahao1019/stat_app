import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt
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
 
    # Add Row and Column header
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole: # more roles
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
 
    # Slots:
    def fileExit(self):
        self.close()
 
    def fileOpen(self):
        home_dir = str(Path.home())
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
            "", "EXCEL files (*.xlsx *.xls);;Text files (*.txt);;Images (*.png *.xpm *.jpg)")
        # print(fname[0])
        if fname[0]:
            self.df = pd.read_excel(fname[0], index_col = None, header = 0)
            self.model = TableModel(self.df)
            self.table.setModel(self.model)
 
            self.label_variable.setText(str(self.df.shape[1]))
            self.label_size.setText(str(self.df.shape[0]))
            self.comboBox_col.clear()
            self.comboBox_col.addItems(self.df.columns)
 
            self.update_plt1()
            self.update_plt2()
             
    def update_plt1(self):
        self.plt1.clear()
        y, x = np.histogram(self.df[self.df.columns[0]])
        # self.plt1.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        barItem = pg.BarGraphItem(x = x[0:len(y)-1], height = y, width = (x.max()-x.min())/len(x), brush=(107,200,224))
        self.plt1.addItem(barItem)
        self.plt1.setTitle(self.df.columns[0])
 
    def update_plt2(self):
        self.plt2.clear()
        if isinstance(self.df[self.df.columns[0]][0], str) or isinstance(self.df[self.df.columns[1]][0], str) :
            self.plt2.setLabel('bottom',"")   
            self.plt2.setLabel('left',"")
            return
        else :
        # if self.df[self.df.columns[0]][0]== float and self.df[self.df.columns[1]][0]== float :
            self.plt2.plot(self.df[self.df.columns[0]], self.df[self.df.columns[1]], pen=None, symbol='o', symbolSize=5)
            self.plt2.setLabel('bottom',self.df.columns[0])   
            self.plt2.setLabel('left',self.df.columns[1])   
         
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()