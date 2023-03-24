from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
import matplotlib.image as mpimg
import pyqtgraph as pg
import sys
import os
 
class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, *args, **kwargs,):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.s = 1
        self.img_dir = "../images/"
        self.img_name = os.listdir(self.img_dir)
 
        # Load the UI Page by PyQt6
        uic.loadUi('app_hw_1.ui', self)
        self.setWindowTitle('Show images on the label widget')
        # app一打開先顯示圖片
        self.image = mpimg.imread(self.img_dir + '/' + self.img_name[0])
        self.img_item = pg.ImageItem(self.image, axisOrder='row-major')
        self.graphWidget.addItem(self.img_item)
        self.graphWidget.invertY(True)
        self.graphWidget.setAspectLocked(lock=True, ratio=1)
 
        # Signals
        self.pBut_first.clicked.connect(self.showImg1)
        self.pBut_previous.clicked.connect(self.showImg2)
        self.pBut_next.clicked.connect(self.showImg3)
        self.pBut_last.clicked.connect(self.showImg4)

# Slots
    def showImg1(self):
        self.graphWidget.clear()
        image = mpimg.imread(self.img_dir + '/' + self.img_name[0])
        img_item = pg.ImageItem(image, axisOrder='row-major')
        self.graphWidget.addItem(img_item)
        self.graphWidget.invertY(True)
        self.graphWidget.setAspectLocked(lock=True, ratio=1)
        self.label_cap.setText('第 1 頁')
        self.s = 1

    def showImg2(self):
        if self.s > 1:
            self.s -= 1
            self.graphWidget.clear()
            image = mpimg.imread(self.img_dir + '/' + self.img_name[self.s-1])
            img_item = pg.ImageItem(image, axisOrder='row-major')
            self.graphWidget.addItem(img_item)
            self.graphWidget.invertY(True)
            self.graphWidget.setAspectLocked(lock=True, ratio=1)
            self.label_cap.setText(f'第 {self.s} 頁')
        else:
            self.graphWidget.clear()
            image = mpimg.imread(self.img_dir + '/' + self.img_name[0])
            img_item = pg.ImageItem(image, axisOrder='row-major')
            self.graphWidget.addItem(img_item)
            self.graphWidget.invertY(True)
            self.graphWidget.setAspectLocked(lock=True, ratio=1)
            self.label_cap.setText(f'第 {1} 頁')
            self.s = 1

    def showImg3(self):
        if self.s < len(self.img_name):
            self.s += 1
            self.graphWidget.clear()
            image = mpimg.imread(self.img_dir + '/' + self.img_name[self.s-1])
            img_item = pg.ImageItem(image, axisOrder='row-major')
            self.graphWidget.addItem(img_item)
            self.graphWidget.invertY(True)
            self.graphWidget.setAspectLocked(lock=True, ratio=1)
            self.label_cap.setText(f'第 {self.s} 頁')
        else:
            self.graphWidget.clear()
            image = mpimg.imread(self.img_dir + '/' + self.img_name[len(self.img_name)-1])
            img_item = pg.ImageItem(image, axisOrder='row-major')
            self.graphWidget.addItem(img_item)
            self.graphWidget.invertY(True)
            self.graphWidget.setAspectLocked(lock=True, ratio=1)
            self.label_cap.setText(f'第 {len(self.img_name)} 頁')
            self.s = len(self.img_name)

    def showImg4(self):
        self.graphWidget.clear()
        image = mpimg.imread(self.img_dir + '/' + self.img_name[len(self.img_name)-1])
        img_item = pg.ImageItem(image, axisOrder='row-major')
        self.graphWidget.addItem(img_item)
        self.graphWidget.invertY(True)
        self.graphWidget.setAspectLocked(lock=True, ratio=1)
        self.label_cap.setText(f'第 {len(self.img_name)} 頁')
        self.s = len(self.img_name)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()