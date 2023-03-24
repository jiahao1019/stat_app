from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
 
class MyWindow(QMainWindow): # inherit QMainWindow that provides a main application window
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 400, 320)
        self.setWindowTitle('Hello Title')
         
        self.label = QtWidgets.QLabel(self) # self = mainwindow
        self.label.setText('This is my first Label')
        self.label.setGeometry(0, 0, 200,20) # (x, y, width, length)
        self.label.move(200, 100)
        self.label.setStyleSheet("border: 1px solid red;")
        self.label.adjustSize()
 
        pbut = QtWidgets.QPushButton(self)
        pbut.setText('Push Me')
        # signal
        pbut.clicked.connect(self.pushme)
 
    # slot
    def pushme(self):
        self.label.setText('My second text')
        self.label.adjustSize()

def main():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()