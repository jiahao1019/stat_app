from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
import sys
import os
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs,):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        # self.picName = ['ntpu', 'ntpu_stone', 'ntpu_library', 'ntpu_flower', 'ntpu_lake']
        self.s = 1
        self.file_src = "../images/"
        self.picName = os.listdir(self.file_src)
 
        # Load the UI Page by PyQt6
        uic.loadUi('app_hw_1.ui', self)
        self.setWindowTitle('Show images on the label widget')
        self.label_Img.setPixmap(QPixmap(u"../images/" + self.picName[0]))
 
        # Signals
        self.pBut_first.clicked.connect(self.showImg1)
        self.pBut_previous.clicked.connect(self.showImg2)
        self.pBut_next.clicked.connect(self.showImg3)
        self.pBut_last.clicked.connect(self.showImg4)

# Slots
    def showImg1(self):
        self.label_Img.setPixmap(QPixmap(u"../images/" + self.picName[0]))
        self.label_cap.setText('第 1 頁')
        self.s = 1

    def showImg2(self):
        if self.s > 1:
            self.s -= 1
            self.label_Img.setPixmap(QPixmap(u"../images/" + self.picName[self.s-1]))
            self.label_cap.setText(f'第 {self.s} 頁')
        else:
            self.label_Img.setPixmap(QPixmap(u"../images/" + self.picName[0]))
            self.label_cap.setText(f'第 {1} 頁')
            self.s = 1

    def showImg3(self):
        if self.s < len(self.picName):
            self.s += 1
            self.label_Img.setPixmap(QPixmap(u"../images/" + self.picName[self.s-1]))
            self.label_cap.setText(f'第 {self.s} 頁')
        else:
            self.label_Img.setPixmap(QPixmap(u"../images/" + self.picName[len(self.picName)-1]))
            self.label_cap.setText(f'第 {len(self.picName)} 頁')
            self.s = len(self.picName)

    def showImg4(self):
        self.label_Img.setPixmap(QPixmap(u"../images/" + self.picName[len(self.picName)-1]))
        self.label_cap.setText(f'第 {len(self.picName)} 頁')
        self.s = len(self.picName)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()