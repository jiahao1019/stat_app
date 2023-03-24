# 2023/03/01
from PyQt6 import QtWidgets, uic
import sys
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        #Load the UI Page by PyQt6
        uic.loadUi('app_0301_1.ui', self)
        self.setWindowTitle('Add more components')
         
        # signal
        self.go_button.clicked.connect(self.go)
        self.greeting.currentIndexChanged.connect(self.go)
        self.recipient.returnPressed.connect(self.go)
     
    # slot
    def go(self):
        str1 = self.greeting.currentText()
        str2 = self.recipient.text()
        self.greet_rep.setText(str1 + ' ' + str2)
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()