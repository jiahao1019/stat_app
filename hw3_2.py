from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests, json, time, datetime, os, sys
import urllib.request
import pyqtgraph as pg
import matplotlib.image as mpimg
import sys, os, io, folium


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
         
        uic.loadUi('hw3_Main.ui', self)
        self.setWindowTitle('氣象資料')
        self.data = self.getData()
        self.showData()
        self.TempData()
        self.RainData()
        self.CloudData()
        self.loc_coordinate = {'台北市':(25.05869, 121.54250), '新北市':(24.94475, 121.37080), '桃園市':(24.99093, 121.29835), '新竹縣':(24.84108, 121.01699),
                               '新竹市':(24.80038, 120.96913), '苗栗縣':(24.56134, 120.82208), '台中市':(24.13709, 120.68559), '彰化縣':(24.05166, 120.51680),
                               '雲林縣':(23.71626, 120.43108), '嘉義縣':(23.44922, 120.25518), '台南市':(23.00336, 120.21006), '高雄市':(22.63051, 120.30180),
                               '屏東縣':(22.55222, 120.53658), '台東縣':(22.80632, 121.09749), '花蓮縣':(23.98621, 121.60212), '宜蘭縣':(24.75751, 121.75251),
                               '南投縣':(23.96588, 120.96658), '澎湖縣':(23.56364, 119.61718), '金門縣':(24.44725, 118.38002), '連江縣':(26.15861, 119.95228),
                               '基隆市':(25.12852, 121.73937), '嘉義市':(23.47932, 120.44973)}
        self.country_num = {'台北市':63, '新北市':65, '桃園市':68, '新竹縣':10004, '新竹市':10018, '苗栗縣':10005, '台中市':66, '彰化縣':10007,
                            '雲林縣':10009, '嘉義縣':10010, '台南市':67, '高雄市':64, '屏東縣':10013, '台東縣':10014, '花蓮縣':10015, '宜蘭縣':10002,
                            '南投縣':10008, '澎湖縣':10016, '金門縣':'09020', '連江縣':'09007', '基隆市':10017, '嘉義市':10020}
        self.show_map()
        # self.pBut.clicked.connect(self.get_reflectivity)
        self.cBox_city.currentIndexChanged.connect(self.showData)
        self.pBut_rain.clicked.connect(self.showbigimg)
        self.pBut_temp.clicked.connect(self.showbigimg_temp)
    
    # 取得雷達回波圖
    def RainData(self):
        path_ = 'images'
        img_dir = "images/"
        if not os.path.exists(path_) :
            os.mkdir(path_)
        self.graphWidget.clear()
        url = 'https://www.cwb.gov.tw/V8/C/W/OBS_Radar_rain.html'
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = soup.find_all("div", class_ = "zoomHolder")
        picture = 'https://www.cwb.gov.tw' + results[0].img.get('src')
        img = requests.get(picture)
        # img = requests.get(picture)
        with open(img_dir + "picture.jpg", "wb") as file:
            file.write(img.content)

        image = mpimg.imread(img_dir + 'picture.jpg')
        img_item = pg.ImageItem(image, axisOrder='row-major')   
        self.graphWidget.addItem(img_item)
        self.graphWidget.invertY(True)
        self.graphWidget.hideAxis('left')
        self.graphWidget.hideAxis('bottom')
        self.graphWidget.getAxis('bottom').setTicks('')
        self.graphWidget.getAxis('left').setTicks('')
        self.graphWidget.setAspectLocked(lock=True, ratio=1)
        os.remove(img_dir + "picture.jpg")

    def TempData(self):
        path_ = 'images'
        img_dir = "images/"
        if not os.path.exists(path_) :
                os.mkdir(path_)

        self.graphWidget_temp.clear()
        if int(time.strftime("%M")) > 15:
            rightnow = time.strftime("%Y-%m-%d_%H00")
        else:
            rightnow = (datetime.datetime.now() + datetime.timedelta(hours = -1)).strftime("%Y-%m-%d_%H00")
        picture = f'https://www.cwb.gov.tw/Data/temperature/{rightnow}.GTP8.jpg'
        img = requests.get(picture)
        # results
        with open(img_dir + "temp.jpg", "wb") as file:
            file.write(img.content)

        image = mpimg.imread(img_dir + 'temp.jpg')
        img_item = pg.ImageItem(image, axisOrder='row-major')   
        self.graphWidget_temp.addItem(img_item)
        self.graphWidget_temp.invertY(True)
        self.graphWidget_temp.hideAxis('left')
        self.graphWidget_temp.hideAxis('bottom')
        self.graphWidget_temp.getAxis('bottom').setTicks('')
        self.graphWidget_temp.getAxis('left').setTicks('')
        self.graphWidget_temp.setAspectLocked(lock = True, ratio=1)
        os.remove(img_dir + "temp.jpg")

    def CloudData(self):
        path_ = 'images'
        img_dir = "images/"
        if not os.path.exists(path_) :
                os.mkdir(path_)

        self.graphWidget_cloud.clear()
        # if int(time.strftime("%M")) > 15:
        #     rightnow = time.strftime("%Y-%m-%d_%H00")
        # else:
        #     rightnow = (datetime.datetime.now() + datetime.timedelta(hours = -1)).strftime("%Y-%m-%d_%H00")
        picture = 'https://www.cwb.gov.tw/Data/satellite/TWI_IR1_CR_800/TWI_IR1_CR_800.jpg'
        img = requests.get(picture)
        # results
        with open(img_dir + "cloud.jpg", "wb") as file:
            file.write(img.content)

        image = mpimg.imread(img_dir + 'cloud.jpg')
        img_item = pg.ImageItem(image, axisOrder='row-major')   
        self.graphWidget_cloud.addItem(img_item)
        self.graphWidget_cloud.invertY(True)
        self.graphWidget_cloud.hideAxis('left')
        self.graphWidget_cloud.hideAxis('bottom')
        self.graphWidget_cloud.getAxis('bottom').setTicks('')
        self.graphWidget_cloud.getAxis('left').setTicks('')
        self.graphWidget_cloud.setAspectLocked(lock = True, ratio=1)
        os.remove(img_dir + "cloud.jpg")

    def showbigimg(self):
        self.anotherwindow = AnotherWindow()
        for i in ['日累積雨量', '樹林雷達回波', '南屯雷達回波', '林園雷達回波']:
            self.anotherwindow.cBox_rain.addItem(str(i))
        self.anotherwindow.passInfo()
        self.anotherwindow.show()

    def showbigimg_temp(self):
        self.anotherwindow = AnotherWindow()
        for i in ['溫度分布圖', '紫外線觀測']:
            self.anotherwindow.cBox_rain.addItem(str(i))
        self.anotherwindow.passInfo()
        self.anotherwindow.show()

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
         
        self.cBox_city.addItems(city)
        return data
    
    def showData(self):
        n, m = 3, 5
        cityName = self.cBox_city.currentText()
        cityIdx = self.cBox_city.currentIndex() 
        # 先定位資料所在的結構層次，再依次取用
        tmp = self.data['records']['location'][cityIdx]['weatherElement']
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


    def show_map(self):
        m = folium.Map(tiles='Stamen Terrain', zoom_start = 7, location = (24.13709, 120.68559))
        # save map data to data object
        data = io.BytesIO()
        # folium.Marker(location = coordinate).add_to(m) # 插入圖標
        for i in range(len(self.loc_coordinate)):
            coordinate = list(self.loc_coordinate.values())[i]
            country_id = list(self.country_num.values())[i]
            country_name = list(self.country_num.keys())[i]
            popup = folium.Popup(f"<a href = https://www.cwb.gov.tw/V8/C/W/County/County.html?CID={country_id}>{country_name}預報</a>",
                                 min_width=60, max_width=60)
            folium.Marker(location = coordinate, tooltip = list(self.loc_coordinate.keys())[i], 
                          popup = popup).add_to(m)
        m.save(data, close_file = False)
 
        webView = QWebEngineView()  # a QWidget
        webView.setHtml(data.getvalue().decode())
 
        # clear the current widget in the verticalLayout before adding one
        if self.verticalLayout_3.itemAt(0) : # if any existing widget
            self.verticalLayout_3.itemAt(0).widget().setParent(None)
        # add a widget with webview inside the vertivalLayout component
        self.verticalLayout_3.addWidget(webView, 0) # at position 0


# 跳出子視窗
class AnotherWindow(QWidget):
    # create a customized signal 
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self):
        super().__init__()
        uic.loadUi('hw3_sub_rain.ui', self)

        # Signal
        self.p_But_back.clicked.connect(self.back)
        self.cBox_rain.currentIndexChanged.connect(self.passInfo) 
        

    def passInfo(self):
        path_ = 'images'
        img_dir = "images/"
        if not os.path.exists(path_) :
                os.mkdir(path_)
        if self.cBox_rain.currentText() == '溫度分布圖':
            self.graphWidget_rain.clear()
            if int(time.strftime("%M")) > 15:
                rightnow = time.strftime("%Y-%m-%d_%H00")
            else:
                rightnow = (datetime.datetime.now() + datetime.timedelta(hours = -1)).strftime("%Y-%m-%d_%H00")
            picture = f'https://www.cwb.gov.tw/Data/temperature/{rightnow}.GTP8.jpg'
            img = requests.get(picture)
            # results
            with open(img_dir + "temp.jpg", "wb") as file:
                file.write(img.content)

            image = mpimg.imread(img_dir + 'temp.jpg')
            img_item = pg.ImageItem(image, axisOrder='row-major')   
            self.graphWidget_rain.addItem(img_item)
            self.graphWidget_rain.invertY(True)
            self.graphWidget_rain.hideAxis('left')
            self.graphWidget_rain.hideAxis('bottom')
            self.graphWidget_rain.getAxis('bottom').setTicks('')
            self.graphWidget_rain.getAxis('left').setTicks('')
            self.graphWidget_rain.setAspectLocked(lock = True, ratio=1)
            os.remove(img_dir + "temp.jpg")
        
        elif self.cBox_rain.currentText() == '紫外線觀測':
            self.graphWidget_rain.clear()
            picture = 'https://www.cwb.gov.tw/Data/UVI/UVI_CWB.png'
            img = requests.get(picture)
            # results
            with open(img_dir + "UVI.jpg", "wb") as file:
                file.write(img.content)

            image = mpimg.imread(img_dir + 'UVI.jpg')
            img_item = pg.ImageItem(image, axisOrder='row-major')   
            self.graphWidget_rain.addItem(img_item)
            self.graphWidget_rain.invertY(True)
            self.graphWidget_rain.hideAxis('left')
            self.graphWidget_rain.hideAxis('bottom')
            self.graphWidget_rain.getAxis('bottom').setTicks('')
            self.graphWidget_rain.getAxis('left').setTicks('')
            self.graphWidget_rain.setAspectLocked(lock = True, ratio=1)
            os.remove(img_dir + "UVI.jpg")

        elif self.cBox_rain.currentText() == '日累積雨量':
            self.graphWidget_rain.clear()
            if int(time.strftime("%M")) > 20:
                rightnow = time.strftime("%Y-%m-%d_%H00")
            else:
                rightnow = (datetime.datetime.now() + datetime.timedelta(hours = -1)).strftime("%Y-%m-%d_%H00")
            picture = f'https://www.cwb.gov.tw/Data/rainfall/{rightnow}.QZJ8.jpg'
            img = requests.get(picture)
            # results
            with open(img_dir + "rain.jpg", "wb") as file:
                file.write(img.content)

            image = mpimg.imread(img_dir + 'rain.jpg')
            img_item = pg.ImageItem(image, axisOrder='row-major')   
            self.graphWidget_rain.addItem(img_item)
            self.graphWidget_rain.invertY(True)
            self.graphWidget_rain.hideAxis('left')
            self.graphWidget_rain.hideAxis('bottom')
            self.graphWidget_rain.getAxis('bottom').setTicks('')
            self.graphWidget_rain.getAxis('left').setTicks('')
            self.graphWidget_rain.setAspectLocked(lock=True, ratio=1)
            os.remove(img_dir + "rain.jpg")
        else:
            if self.cBox_rain.currentText() == '樹林雷達回波':
                location = 'SL'
            if self.cBox_rain.currentText() == '南屯雷達回波':
                location = 'NT'
            if self.cBox_rain.currentText() == '林園雷達回波':
                location = 'LY' 
            self.graphWidget_rain.clear()
                # url = 'https://www.cwb.gov.tw/V8/C/W/OBS_Radar_rain.html'
                # resp = requests.get(url)
                # soup = BeautifulSoup(resp.text, 'html.parser')
                # results = soup.find_all("div", class_ = "zoomHolder")     # /Data/radar_rain/CV1_RCSL_3600/CV1_RCSL_3600.png
            picture = f'https://www.cwb.gov.tw/Data/radar_rain/CV1_RC{location}_3600/CV1_RC{location}_3600.png' # + results[0].img.get('src')
            img = requests.get(picture)
                # img = requests.get(picture)
            with open(img_dir + "picture.jpg", "wb") as file:
                file.write(img.content)

            image = mpimg.imread(img_dir + 'picture.jpg')
            img_item = pg.ImageItem(image, axisOrder='row-major')   
            self.graphWidget_rain.addItem(img_item)
            self.graphWidget_rain.invertY(True)
            self.graphWidget_rain.hideAxis('left')
            self.graphWidget_rain.hideAxis('bottom')
            self.graphWidget_rain.getAxis('bottom').setTicks('')
            self.graphWidget_rain.getAxis('left').setTicks('')
            self.graphWidget_rain.setAspectLocked(lock=True, ratio=1)
            os.remove(img_dir + "picture.jpg")
  
    def back(self):
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()