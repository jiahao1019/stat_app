from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
import sys
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        self.picName = ["ntpu", "ntpu_stone", "ntpu_library"]
 
        # Load the UI Page by PyQt6
        uic.loadUi('app_0308_2.ui', self)
        self.label_Img.setPixmap(QPixmap(u"../images/" + self.picName[0]))
        self.setWindowTitle('Show images on the label widget')
        url = "https://new.ntpu.edu.tw/"
        self.label_ntpu.setText(f'<a href="{url}">{url}</a>')# should have quotes around url, i.e. href="https://...."
        # self.label_ntpu.setOpenExternalLinks(True) # can be set True in Designer
 
        # Signals
        self.comboBox_ImgName.currentIndexChanged.connect(self.showImg)
        self.pBut_exit.clicked.connect(self.close)
 
# Slots
    def showImg(self, s):
        self.label_Img.setPixmap(QPixmap(u"../images/" + self.picName[s]))
        self.label_cap.setText(self.comboBox_ImgName.itemText(s)) # set Label text
        # self.label_cap.setText(self.comboBox_ImgName.currentText())
     
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()