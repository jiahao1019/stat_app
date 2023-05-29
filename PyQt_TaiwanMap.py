from PyQt6.QtWebEngineWidgets import QWebEngineView # pip install PyQt6-WebEngine
from PyQt6 import QtWidgets, uic
import folium # pip install folium
from folium import GeoJson
import json
import sys
import io
 
"""
Folium in PyQt6
"""
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
         
        uic.loadUi('PyQt_Designer_GeoMap_border.ui', self)
        f = open('geo_taiwan.json',encoding='utf8')
        self.data = json.load(f)
        self.get_city()
        self.show_map()
 
        #signals
        self.comboBox_city.currentIndexChanged.connect(self.show_map)
 
    def show_map(self):
        idx = self.comboBox_city.currentIndex()
        self.county = self.data['features'][idx]['geometry']
        m = folium.Map(
            # tiles='Stamen Terrain', # tiles = Stamen Toner, CartoDB positron, Cartodb dark_matter, Stamen Watercolor or Stamen Terrain
            zoom_start = 7, # 適當的放大倍數能看到全島
            location = (23.73, 120.96) # 以台灣中部山脈為中心點
        ) 
        # m = folium.Map(width="%100",weight="%100") # 完整的世界地圖
        GeoJson(self.county,
            style_function=lambda feature: {
                'fillColor': '#adff2f',
                'color':'yellow'}).add_to(m)
        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file = False)
        self.webEngineView.setHtml(data.getvalue().decode())
 
    # 取得檔案中縣市的名稱
    def get_city(self):
        cities = []
        for i in range(len(self.data['features'])):
            cities.append(self.data['features'][i]['properties']['name'])
        self.comboBox_city.addItems(cities)
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()