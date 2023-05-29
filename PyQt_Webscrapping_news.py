from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtGui import QPixmap
from bs4 import BeautifulSoup
import urllib.request
import requests
import sys
import os
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
         
        uic.loadUi('PyQt_Webscrapping_news.ui', self)
        self.setWindowTitle('自由電子報新聞')
        self.news_classification = {"即時":"","熱門":"popular","政治":"politics","社會":"society","生活":"life"}
        self.newsSearch()
         
        # Signals
        self.comboBox_class.currentIndexChanged.connect(self.newsSearch)
        self.lineEdit_keyword.returnPressed.connect(self.searchByKeyword)
    # Slots
    def newsSearch(self):
        url = "https://news.ltn.com.tw/list/breakingnews/"
        classification = self.news_classification[self.comboBox_class.currentText()]
        url = url + classification
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("img", class_="lazy_imgs_ltn", limit=4)
        image_links = [result.get("data-src") for result in results]
        print(image_links)
        self.show_image(image_links)
        self.titleSearch()
 
    def titleSearch(self):
        url = "https://news.ltn.com.tw/list/breakingnews/"
        classification = self.news_classification[self.comboBox_class.currentText()]
        url = url + classification
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("h3", class_="title", limit=4)
 
        for i in range(len(results)):
            title = results[i].text
            setlabel = "self.title_"+str(i+1)+".setText(title)"
            exec(setlabel)
         
    def searchByKeyword(self):
        keyword = self.lineEdit_keyword
     
    def show_image(self, image_links):
        for index, link in enumerate(image_links):
            data = urllib.request.urlopen(link).read()
            image = QtGui.QImage()
            image.loadFromData(data)
            setlabel = "self.img_"+str(index+1)+".setPixmap(QPixmap(image))"
            exec(setlabel)
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()