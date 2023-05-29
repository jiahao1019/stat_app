from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtCore import Qt
import pandas as pd
import numpy as np
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
 
            # if orientation == Qt.Orientation.Vertical:
            #     return str(self._data.index[section])
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
         
        uic.loadUi('PyQt_Webscrapping_CWB_API.ui', self)
        self.data = self.getData()
        self.showData()
         
        # Signals
        self.comboBox_city.currentIndexChanged.connect(self.showData)
        self.pBut_exit.clicked.connect(self.close)
     
    # Slots
    def getData(self):
        api = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/'
        dataCode = 'F-C0032-001' # 臺灣各縣市天氣預報資料及國際都市天氣預報

        auth = "Authorization=CWB-69F62321-97EC-4E69-8267-47CBD6E8B929"
        url = api + dataCode + "?"+ auth + "&format=JSON"
        res = requests.get(url)
        data = res.json()
        # 首先取得縣市名稱並寫入 comboBox
        city = []
        for i in range(len(data['records']['location'])):
            city.append(data['records']['location'][i]['locationName'])
         
        self.comboBox_city.addItems(city)
        return data
    
    def showData(self):
        n, m = 3, 5
        cityName = self.comboBox_city.currentText()
        cityIdx = self.comboBox_city.currentIndex() 
        # 先定位資料所在的結構層次，再依次取用
        tmp =self.data['records']['location'][cityIdx]['weatherElement']
        d = []
        for i in range(n):
            d.append(tmp[0]['time'][i]['startTime'])
            for j in range(m):
                d.append(tmp[j]['time'][i]['parameter']['parameterName'])
         
        self.df = pd.DataFrame(np.reshape(d, (n,m+1)))
        self.df.columns = ['時間', '天氣現象','降雨機率(%)','最低溫度','舒適度','最高溫度']
        self.model = TableModel(self.df)
        self.tableView.setModel(self.model)
        # self.tableView.resizeColumnsToContents
        self.tableView.resizeColumnToContents(0)
        self.tableView.resizeColumnToContents(1)
        self.tableView.resizeColumnToContents(2)
        self.tableView.resizeColumnToContents(3)
        self.tableView.resizeColumnToContents(5)
         
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()