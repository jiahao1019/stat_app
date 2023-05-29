from PyQt6.QtWebEngineWidgets import QWebEngineView # pip install PyQt6-WebEngine
from PyQt6 import QtWidgets, uic
import folium # pip install folium
import sys, io
import pandas as pd

class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
         
        uic.loadUi('PyQt_Designer_GeoMap.ui', self)
 
        df = pd.read_excel(r'C:\Users\user\Downloads\cow_farm.xlsx', sheet_name = 'cow_farm')
        m = folium.Map(tiles = 'Stamen Terrain', zoom_start = 8, location = (df['緯度'][0], df['經度'][0]))
        data = io.BytesIO()

        for i in range(len(df)):
            coordinate = (df['緯度'][i], df['經度'][i])
            popup = folium.Popup('負責人:' + df['負責人'][i], min_width=100, max_width=100)
            folium.CircleMarker(location = coordinate, radius = 3, color = 'red', fill_color = 'red',
                                tooltip = df['牧場'][i], popup = popup).add_to(m)

        m.save(data, close_file = False)

        webView = QWebEngineView()  # a QWidget
        webView.setHtml(data.getvalue().decode())

        # clear the current widget in the verticalLayout before adding one
        if self.verticalLayout.itemAt(0) : # if any existing widget
            self.verticalLayout.itemAt(0).widget().setParent(None)
        # add a widget with webview inside the vertivalLayout component
        self.verticalLayout.addWidget(webView, 0) # at position 0

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()