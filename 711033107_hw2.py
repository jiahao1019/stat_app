from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
import matplotlib.image as mpimg
import pyqtgraph as pg
import pandas as pd
import sqlite3
from sqlite3 import Error
import sys
import os
 
class TableModel(QtCore.QAbstractTableModel):
 
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
 
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()] #pandas's iloc method
            return str(value)
 
        if role == Qt.ItemDataRole.TextAlignmentRole:          
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignHCenter
         
        if role == Qt.ItemDataRole.BackgroundRole and (index.row()%2 == 0):
            return QtGui.QColor('antiquewhite')
 
    def rowCount(self, index):
        return self._data.shape[0]
 
    def columnCount(self, index):
        return self._data.shape[1]
 
    # Add Row and Column header
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole: # more roles
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
 
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self):
        super().__init__()
        uic.loadUi('711033107_hw2_Main.ui', self)
        self.table = self.tableView
        self.authors = ''
        self.page = 1
        self.one_page_rows = 10
        self.rows = ''
         
        # database = r'C:\Users\user\Downloads\SQL\test.sqlite'
        database = 'test.sqlite'
        # create a database connect
        self.conn = create_connection(database)
        self.setWindowTitle('Paper Query System')
 
        # Signals
        self.actionEXIT.triggered.connect(self.appEXIT)
        self.pBut_query.clicked.connect(self.searchByAuthor)
        self.table.doubleClicked.connect(self.call_subWin)
        self.pBut_first.clicked.connect(self.show_first)
        self.pBut_previous.clicked.connect(self.show_previous)
        self.pBut_next.clicked.connect(self.show_next)
        self.pBut_last.clicked.connect(self.show_last)
        self.cBox.currentIndexChanged.connect(self.set_page)

    # Slots
    def searchByAuthor(self):  #, Title, EventType, Abstract, PaperText
        self.page = 1
        sql = 'select B.Id, Title, EventType, Abstract, PaperText, imgfile from paperauthors A, papers B, authors C where A.paperid = B.id and A.authorid = C.id'
        author = self.lineEdit_author.text()
        title = self.lineEdit_title.text() 

        if (author and title) != '':
            sql = sql + " and C.name like '%" + author + "%' and B.title like '%" + title + "%'"
        if author == '':
            sql = sql + " and B.title like '%" + title + "%'"
        if title == '':
            sql = sql + " and C.name like '%" + author + "%'"

        if self.checkBox_poster.isChecked():
            type1 = "'Poster',"
        else:
            type1 = ''

        if self.checkBox_spotlight.isChecked():
            type2 = "'Spotlight',"
        else:
            type2 = ''

        if self.checkBox_oral.isChecked():
            type3 = "'Oral',"
        else:
            type3 = ''
        
        if (type1 and type2 and type3) == '':
            sql = sql
        if (type1 or type2 or type3) != '':
            sql = sql + f" and B.eventtype in ({type1}{type2}{type3})"
            sql = sql[:-2] + ")"

        with self.conn:
            self.rows = SQLExecute(self, sql)
            # print(len(self.rows))
            if len(self.rows) > 0: 
                ToTableView(self, self.rows)
                self.cBox.addItems(str(i) for i in range(1, (len(self.df)//self.one_page_rows) + 2))
        self.label_counts.setText(str(len(self.rows)))

    def call_subWin(self, mi):
        col_list = list(self.df.columns)
        # display Abstract on TextBrowser, then go fetch author names
        abstract = self.df.iloc[mi.row()+(self.page-1)*10, col_list.index('Abstract')]
        papertext = self.df.iloc[mi.row()+(self.page-1)*10, col_list.index('PaperText')]
        title = self.df.iloc[mi.row()+(self.page-1)*10, col_list.index('Title')]
        show_authors(self, self.df.iloc[mi.row()+(self.page-1)*10, 0])
        img_name = self.df.iloc[mi.row()+(self.page-1)*10, col_list.index('imgfile')]
        self.anotherwindow = AnotherWindow()
        self.anotherwindow.passInfo(abstract, papertext, title, self.authors, img_name)
        self.anotherwindow.show()

    def show_first(self):
        self.page = 1
        ToTableView(self, self.rows)
    
    def show_previous(self):
        if self.page > 1:
            self.page -= 1
            ToTableView(self, self.rows)
        else:
            pass
    
    def show_next(self):
        self.page += 1
        ToTableView(self, self.rows)

    def show_last(self):
        self.page = 'last_page'
        ToTableView(self, self.rows)

    def set_page(self):
        if self.cBox.currentText() == '':
            pass
        else:
            self.page = int(self.cBox.currentText())
            ToTableView(self, self.rows)

    def appEXIT(self):
        self.conn.close() # close database
        self.close() # close app
     
def show_authors(self, paperid):
    sql = "select name from authors A, paperauthors B where B.paperid=" + str(paperid) + " and A.id=B.authorid"
    with self.conn:
        self.rows2 = SQLExecute2(self, sql)
        names = ""
        for row in self.rows2:
            names = names + row[0] +"; "
        self.authors = names

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn
 
def SQLExecute(self, SQL):
    """
    Execute a SQL command
    :param conn: SQL command
    :return: None
    """
    self.cur = self.conn.cursor()
    try:
        self.cur.execute(SQL)
    except Error as e:
        print('error')
        display_message(str(e))
        return None
    rows = self.cur.fetchall()
    if len(rows) == 0:
        display_message('Nothing Found')
    self.cBox.clear()
    return rows

def SQLExecute2(self, SQL):
    """
    Execute a SQL command
    :param conn: SQL command
    :return: None
    """
    self.cur2 = self.conn.cursor()
    try:
        self.cur2.execute(SQL)
    except Error as e:
        display_message(str(e))
        return None
    rows = self.cur2.fetchall()
    return rows

def display_message(message):
    dlg = QMessageBox()
    dlg.setWindowTitle("SQL Information: ")
    dlg.setText(message)
    dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
    buttonY = dlg.button(QMessageBox.StandardButton.Yes)
    buttonY.setText('OK')
    dlg.setIcon(QMessageBox.Icon.Information)
    dlg.exec()

def ToTableView(self, rows):
    """
    Display rows on the TableView in pandas format
    """
    names = [description[0] for description in self.cur.description]  # extract column names
    self.df = pd.DataFrame(rows)
    self.df.columns = names
    self.df.index = range(1, len(rows)+1)
    if self.page == 'last_page':
        self.dff = self.df[(len(self.df)//self.one_page_rows)*self.one_page_rows:len(self.df)]
        self.model = TableModel(self.dff)
        self.table.setModel(self.model)
        self.dff.columns = names
        self.table.resizeColumnToContents(0)
        self.page = len(self.df)//self.one_page_rows + 1
        self.label_page.setText(str(len(self.df)//self.one_page_rows + 1))
        
    elif 1 <= self.page <= (len(self.df)//self.one_page_rows) + 1:
        self.dff = self.df[(self.page-1) * self.one_page_rows : self.page * self.one_page_rows]
        self.model = TableModel(self.dff)
        self.table.setModel(self.model)
        self.dff.columns = names
        self.table.resizeColumnToContents(0)
        self.label_page.setText(str(self.page))

# 跳出子視窗
class AnotherWindow(QWidget):
    # create a customized signal 
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    img_dir = 'NIP2015_Images'

    def __init__(self):
        super().__init__()
        uic.loadUi('711033107_hw2_Sub.ui', self)

        # Signal
        self.p_But_back.clicked.connect(self.back)

    def passInfo(self, abstract, papertext, title, authors, imgfile):
        self.tBrowser_abstract.setText(abstract)
        self.tBrowser_papertext.setText(papertext)
        self.label_title.setText(title)
        self.tBrowser_authors.setText(authors)
        self.graphWidget.clear()
        image = mpimg.imread(self.img_dir + '/' + imgfile)
        img_item = pg.ImageItem(image, axisOrder='row-major')
        self.graphWidget.addItem(img_item)
        self.graphWidget.invertY(True)
        self.graphWidget.getAxis('bottom').setTicks('')
        self.graphWidget.getAxis('left').setTicks('')
        self.graphWidget.hideAxis('left')
        self.graphWidget.hideAxis('bottom')
        self.graphWidget.setBackground((216,216,216))
        self.graphWidget.setAspectLocked(lock=True, ratio=1)
     
    def back(self):
        self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()