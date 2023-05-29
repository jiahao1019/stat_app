from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import pandas as pd
import requests
import sys
import os

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()] #pandas's iloc method
            return str(value)

        if role == Qt.ItemDataRole.TextAlignmentRole:          
            # return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignHCenter
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignLeft
        
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

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        #Load the UI Page by PyQt6
        uic.loadUi('PyQt_Webscrapping_newsJson.ui', self)
        self.url = "https://news.ltn.com.tw/ajax/breakingnews/popular/"
        self.newsSearch()
        
        # Signals
        self.tableView.doubleClicked.connect(self.rowSelected)
        self.comboBox_page.currentIndexChanged.connect(self.newsSearch)
        self.pBut_exit.clicked.connect(self.close)
    
    # Slots
    def newsSearch(self):
        goto_page = self.comboBox_page.currentIndex()
        p = goto_page * 20
        url = self.url + str(goto_page + 1) # from 1 to 10
        response = requests.get(url)
        self.data = response.json().get('data')

        self.df = pd.DataFrame([[self.data[toIdx(p)]['time'], self.data[toIdx(p)]['title'], self.data[toIdx(p)]['type_cn']]], columns=['日期/時間','標題','類別'])
        for i in range(len(self.data)-1):
            self.df.loc[len(self.df.index)] = [self.data[toIdx(p+i+1)]['time'], self.data[toIdx(p+i+1)]['title'], self.data[toIdx(p+i+1)]['type_cn']]

        self.model = TableModel(self.df)
        self.tableView.setModel(self.model)
        self.df.index = range(p+1,len(self.data)+p+1)
        self.tableView.setColumnWidth(0, 120)
        self.tableView.setColumnWidth(1, 250)
        self.tableView.setColumnWidth(2, 50)
        
    def rowSelected(self, mi):
        current_page = self.comboBox_page.currentIndex()
        idx = current_page *20 + mi.row()
        self.textBrowser_summary.setText(self.data[toIdx(idx)]['summary'])
        img_link = self.data[toIdx(idx)]['photo_S']
        img = requests.get(img_link)
        img_dir = "images/"
        with open( img_dir +  "tmp.jpg", "wb") as file:
            file.write(img.content)
        self.label_img.setPixmap(QPixmap(img_dir + 'tmp.jpg'))
        os.remove(img_dir + 'tmp.jpg')
        
def toIdx(p):
    return p if p < 20 else str(p)
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()