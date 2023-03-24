from PyQt6.QtWidgets import QApplication, QWidget, \
    QVBoxLayout, QComboBox, QLineEdit, QPushButton, QLabel
import sys
 
class MyWindow(QWidget): # inherits from QWidget, a convenient widget for an empty window.
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 400, 200)
        # self.setMinimumSize(400, 200)
        self.setWindowTitle('Add more components')
 
        # Add a vertical layout
        self.vbox = QVBoxLayout()
        # The available greetings
        self.greetings = ['hello', 'goodbye', 'heyo']
        # The greeting combo box
        self.greeting = QComboBox(self)
        # Add the greetings
        # list(map(self.greeting.addItem, self.greetings))
        self.greeting.addItems(self.greetings)
        # The recipient textbox
        self.recipient = QLineEdit('world', self)
        # The greeting + recipient
        self.greet_rep = QLabel('Hello World', self)
        self.greet_rep.setStyleSheet("border: 1px solid red;")
        # The Go button
        self.go_button = QPushButton('&Go')
        # signal
        self.go_button.clicked.connect(self.go)
 
        # Add the controls to the vertical layout
        self.vbox.addWidget(self.greeting)
        self.vbox.addWidget(self.recipient)
        self.vbox.addWidget(self.greet_rep)
        # A very stretchy spacer to force the button to the bottom
        self.vbox.addStretch(100)
        self.vbox.addWidget(self.go_button)
        # Use the vertical layout for the current window
        self.setLayout(self.vbox)
     
    # slot
    def go(self):
        str1 = self.greeting.currentText()
        # str1 = self.greetings[self.greeting.currentIndex()]
        str2 = self.recipient.text()
        self.greet_rep.setText(str1 + ' ' + str2)
 
def main():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()