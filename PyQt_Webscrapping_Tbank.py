from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtCore import Qt
from bs4 import BeautifulSoup
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
        uic.loadUi('PyQt_Webscrapping_TaiwanBank.ui', self)
        self.urlSearch()
        # Signals
        self.pBut_search.clicked.connect(self.urlSearch)
        self.pBut_exit.clicked.connect(self.close)
        self.comboBox_money.currentIndexChanged.connect(self.urlSearch)
        self.comboBox_year.currentIndexChanged.connect(self.urlSearch)
        self.comboBox_month.currentIndexChanged.connect(self.urlSearch)
 
    def urlSearch(self):
        money = {"美金":"USD", "歐元":"EUR", "英鎊":"GBP", "日圓":"JPY"}
        url = "https://rate.bot.com.tw/xrt/quote/" #2022-04/USD"
        url = url + self.comboBox_year.currentText() + "-" + self.comboBox_month.currentText()
        url = url + "/" + money[self.comboBox_money.currentText()]
        res = requests.get(url)
        # start html parsing
        soup = BeautifulSoup(res.content, 'html.parser')
 
        table1 = soup.find_all("td",class_="rate-content-cash text-right print_table-cell")
        table2 = soup.find_all("td",class_="rate-content-sight text-right print_table-cell")
        table3 = soup.find_all("td",class_="text-center")
 
        cash = [i.text for i in table1]
        sight = [i.text for i in table2]
        date = [i.text for i in table3]
             
        header = ["日期","現金買入","現金賣出","即期買入","即期賣出"]
        cash = np.reshape(cash, (int(len(cash)/2),2))
        sight = np.reshape(sight, (int(len(sight)/2),2))
        date = np.reshape(date, (int(len(date)/2),2))
 
        self.df = pd.DataFrame(date[:,0])
        self.df = self.df.assign(cashin = cash[:,0], cashout = cash[:,1])
        self.df = self.df.assign(buyin=sight[:,0], soldout=sight[:,1])
        self.df.columns = header
        self.model = TableModel(self.df)
        self.tableView.setModel(self.model)
 
        self.graphicsView.clear()
        self.graphicsView.addLegend(offset = (20,5),labelTextSize = "12pt")
        x = np.arange(len(sight[:,1]))
        # flip data to begin with day 1
        y1 = np.flip(sight[:,0].astype(np.float))
        y2 = np.flip(sight[:,1].astype(np.float))
         
        self.graphicsView.plot(x, y2, pen ='r', symbol ='o', \
            symbolPen ='r', symbolBrush = 0.2, name = header[4])
        self.graphicsView.plot(x, y1, pen ='g', symbol ='x', \
            symbolPen ='g', symbolBrush = 0.2, name = header[3])
        date_short =[i[5::] for i in date[:,0]]
        date_short = np.flip(date_short)
        # xtick = dict(enumerate(date_short))
        # self.graphicsView.getAxis('bottom').setTicks([xtick.items()])
        self.graphicsView.getAxis('bottom').setTicks([[(i, date_short[i]) for i in x[::2]]])
        # self.graphicsView.getAxis('bottom').setTicks([[(i, date_short[i-1]) for i in x]])
        self.graphicsView.setLabel('bottom', date[:,0][0][0:4]+'年')
 
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()