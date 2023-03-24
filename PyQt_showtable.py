import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt
import numpy as np
from scipy.stats import norm
 
 
class TableModel(QtCore.QAbstractTableModel): # custom table model
 
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
 
    def data(self, index, role): # required method
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row(), index.column()]
            return str(round(value,4))
 
        if role == Qt.ItemDataRole.TextAlignmentRole:          
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight # vertical + horizontal
 
        if role == Qt.ItemDataRole.BackgroundRole and index.column() % 2 != 0: # change background color on even column
            return QtGui.QColor('#d8ffdb')
         
        if role == Qt.ItemDataRole.ForegroundRole:
            value = self._data[index.row()][index.column()]
            if value < 0 :
            # if (
            #     (isinstance(value, int) or isinstance(value, float))
            #     and value < 0
            # ):
                return QtGui.QColor('red') # change color if value < 0
             
 
    def rowCount(self, index): # required method
        return self._data.shape[0]
 
    def columnCount(self, index): # required method
        return self._data.shape[1]
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self):
        super().__init__()
        uic.loadUi('PyQtTable_numpy.ui', self)
        self.setWindowTitle('Table View: the numpy version')

        self.lineEdit_size.returnPressed.connect(self.change)
        self.lineEdit_variables.returnPressed.connect(self.change)

        self.table = self.tableView # setp 1:create a QTableView widget
        # prepare data
    def change(self):
        sample = int(self.lineEdit_size.text())
        d = int(self.lineEdit_variables.text())
        Data = norm.rvs(size = (sample, d))

        self.model = TableModel(Data) # step 2:create an instance of custom TableModel object
        self.table.setModel(self.model) # step 3:set Table View with data of TableModel object
        # self.table.resizeColumnsToContents() # adjust column width to textsize
    

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()