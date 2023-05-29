from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtCore import Qt
from bs4 import BeautifulSoup
from datetime import datetime
import numpy  as np
import pandas as pd
import requests
import sys
 
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
            # return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignLeft
         
        if role == Qt.ItemDataRole.BackgroundRole and (index.row()%2 == 0):
            return QtGui.QColor('#fff2d5')
 
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
 
            # if orientation == Qt.Orientation.Vertical:
            #     return str(self._data.index[section])
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('PyQt_Webscrapping_Stock_Table_graph.ui', self)
         
                          
        self.urlSearch()
        # Signals
        self.lineEdit_stock_no.returnPressed.connect(self.urlSearch)
        self.pBut_exit.clicked.connect(self.close)
         
    def urlSearch(self):
        stock_no = self.lineEdit_stock_no.text()
        url = "https://www.twse.com.tw/exchangeReport/FMNPTK?response=html&stockNo="+stock_no
        res = requests.get(url, cert = '', timeout=5)
        soup = BeautifulSoup(res.content, 'html.parser')
        stock_name = soup.find("h2")
        self.label_name.setText(stock_name.text)
 
 
        title = soup.find_all("thead")
        # tmp = title[0].find_all("td")
        headers = []
        for i in title[0].find_all("td"):
            headers.append(i.text)
         
        content = soup.find_all("tbody")
        tmp = content[0].find_all("td")
        deal_info = []
        for i in content[0].find_all("td"):
            deal_info.append(i.text)
         
        deal_info = np.reshape(deal_info, (int(len(deal_info)/len(headers)), len(headers)))
        data = pd.DataFrame(deal_info, columns = headers)
        self.df = pd.DataFrame(data)
        self.model = TableModel(self.df)
        self.tableView.setModel(self.model)
        # for i in range(8):
        #     self.tableView.resizeColumnToContents(i)
        self.tableView.resizeColumnsToContents()
 
        self.graphicsView.clear()
        self.graphicsView.addLegend(offset = (20,5),labelTextSize = "12pt")
        x = np.arange(len(deal_info))
        y = [float(i.replace(',','')) for i in deal_info[:,-1]]
        y_max = [float(i.replace(',','')) for i in deal_info[:,4]]
        y_min = [float(i.replace(',','')) for i in deal_info[:,6]]
         
        self.graphicsView.plot(x, y_max, pen ='g', name = headers[4])
        self.graphicsView.plot(x, y, pen ='r', symbol ='+', \
            symbolPen ='r', symbolBrush = 0.1, name = headers[-1])
        self.graphicsView.plot(x, y_min, pen ='y',  name = headers[6])
         
        date = deal_info[:,0]
        self.graphicsView.getAxis('bottom').setTicks([[(i, date[i]) for i in x[::2]]])
        self.graphicsView.setLabel('bottom', '年度')
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()