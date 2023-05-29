# Show folium map in pyqt6 + Designer
 
from PyQt6.QtWebEngineWidgets import QWebEngineView # pip install PyQt6-WebEngine
from PyQt6 import QtWidgets, uic
import folium # pip install folium
import sys
import io
 
"""
Folium in PyQt6
"""
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
         
        uic.loadUi('PyQt_Designer_GeoMap.ui', self)
 
        # coordinate = (37.8199286, -122.4782551) # 金門大橋
        coordinate1 = (24.944752335627687, 121.3708067871758) # 台北大學
        coordinate2 = (25.058691930742544, 121.54250844112391)
        coordinate3 = (25.05664120926736, 121.53747661711536)
        self.loc_coordinate = {"台北大學三峽校區":coordinate1, 
                               "台北大學民生校區":coordinate2, 
                               "台北大學建國校區":coordinate3 }
        loc = self.comboBox_campus.currentText()
        self.show_map(self.loc_coordinate[loc])
 
        # signals
        self.comboBox_campus.currentIndexChanged.connect(self.which_campus)
 
    def show_map(self, coordinate):
        m = folium.Map(tiles='CartoDB Positron', zoom_start=13, location=coordinate)
        # save map data to data object
        data = io.BytesIO()
        folium.Marker(location = coordinate).add_to(m) # 插入圖標
        m.save(data, close_file = False)
 
        webView = QWebEngineView()  # a QWidget
        webView.setHtml(data.getvalue().decode())
 
        # clear the current widget in the verticalLayout before adding one
        if self.verticalLayout.itemAt(0) : # if any existing widget
            self.verticalLayout.itemAt(0).widget().setParent(None)
        # add a widget with webview inside the vertivalLayout component
        self.verticalLayout.addWidget(webView, 0) # at position 0
     
    def which_campus(self):
        loc = self.comboBox_campus.currentText()
        self.show_map(self.loc_coordinate[loc])
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()