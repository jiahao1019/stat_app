from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
 
def pushme():
    print('clicked...') 
 
def main():
    app = QApplication(sys.argv) 
    win = QMainWindow() 
     
    # Configure the main window
    win.setGeometry(200, 200, 400, 320)
    win.setWindowTitle('Hello Title')
 
    # create a label and its associated properties
    label = QtWidgets.QLabel(win)
    label.setText('This is my first Label')
    label.setGeometry(0, 0, 200,20) # (x, y, width, length)
    label.move(100, 100)
    label.setStyleSheet("border: 1px solid black;")
    label.adjustSize() # to fit the text length
 
    # create a pushbutton
    pbut = QtWidgets.QPushButton(win)
    pbut.setText('Push Me')
    pbut.clicked.connect(pushme)
 
    win.show()
    sys.exit(app.exec())
 
if __name__ == '__main__': # run by itself, not by other application
    main()