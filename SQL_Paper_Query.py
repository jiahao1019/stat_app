from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox 
from PyQt6.QtCore import Qt
import pandas as pd
import sqlite3
from sqlite3 import Error
import sys
 
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
            return QtGui.QColor('#d8ffdb')
 
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
        uic.loadUi('PySQLite_Designer_3.ui', self)
        self.table = self.tableView
         
        database = r'C:\Users\user\Downloads\SQL\database.sqlite'
        # create a database connect
        self.conn = create_connection(database)
        self.setWindowTitle('Paper Query System')
 
        # Signals
        self.actionEXIT.triggered.connect(self.appEXIT)
        self.lineEdit_author.returnPressed.connect(self.searchByAuthor)
        self.p_But_by_author.clicked.connect(self.searchByAuthor)
        self.lineEdit_title.returnPressed.connect(self.searchByTitle)
        self.p_But_by_title.clicked.connect(self.searchByTitle)
        self.table.doubleClicked.connect(self.rowSelected)
        self.actionSave_Data.triggered.connect(self.saveData)
         
    # Slots
    def searchByAuthor(self):
        author_key = self.lineEdit_author.text()
        sql = "select id"
         
        if self.checkBox_title.isChecked():
            sql = sql + ",title"
        if self.checkBox_type.isChecked():
            sql = sql + ",eventtype"
        if self.checkBox_abstract.isChecked():
            sql = sql + ",abstract"   
        if self.checkBox_text.isChecked():
            sql = sql + ", papertext"
         
        sql = sql + " from papers where author like '%"+author_key+"%'"
        with self.conn:
            self.rows = SQLExecute(self, sql)
            if len(self.rows) > 0: 
                ToTableView(self, self.rows)


    def searchByTitle(self):
        title_key = self.lineEdit_title.text()
        # sql = "select id, title, eventtype, abstract from papers where title like '%"+title_key+"%'"
        sql = "select id"
         
        if self.checkBox_title.isChecked():
            sql = sql + ",title"
        if self.checkBox_type.isChecked():
            sql = sql + ",eventtype"
        if self.checkBox_abstract.isChecked():
            sql = sql + ",abstract"   
        if self.checkBox_text.isChecked():
            sql = sql + ", papertext"
         
        sql = sql + " from papers where title like '%" + title_key + "%'"
        with self.conn:
            self.rows = SQLExecute(self, sql)
            if len(self.rows) > 0: 
                ToTableView(self, self.rows)
     
    def rowSelected(self, mi):
        print([mi.row(), mi.column()])
        if 'Abstract' in self.df.columns:
            col_list = list(self.df.columns)
        else:
            print('No Abstract from the Query')
            return
        # display Abstract on TextBrowser, then go fetch author names
        self.textBrowser_abstract.setText(self.df.iloc[mi.row(), col_list.index('Abstract')])
        show_authors(self, self.df.iloc[mi.row(), 0])
 
    def saveData(self):
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', 
            "", "EXCEL files (*.xlsx)")
        if len(fname) != 0:
            self.df.to_excel(fname)
 
    def appEXIT(self):
        self.conn.close() # close database
        self.close() # close app
     
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
    self.cur.execute(SQL)
    rows = self.cur.fetchall()
 
    if len(rows) == 0: # nothing found
        # raise a messageBox here
        dlg = QMessageBox(self)
        dlg.setWindowTitle("SQL Information: ")
        dlg.setText("No data match the query !!!")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
        buttonY = dlg.button(QMessageBox.StandardButton.Yes)
        buttonY.setText('OK')
        dlg.setIcon(QMessageBox.Icon.Information)
        button = dlg.exec()
        # return
    return rows
 
def ToTableView(self, rows):
    """
    Display rows on the TableView in pandas format
    """
    names = [description[0] for description in self.cur.description]# extract column names
    self.df = pd.DataFrame(rows)
    self.model = TableModel(self.df)
    self.table.setModel(self.model)
    self.df.columns = names
    self.df.index = range(1, len(rows)+1)
     
def show_authors(self, paperid):
    sql = "select name from authors A, paperauthors B where B.paperid="+str(paperid)+" and A.id=B.authorid"
    with self.conn:
        self.rows = SQLExecute(self, sql)
        names =""
        for row in self.rows:
            names = names + row[0] +"; "
        self.textBrowser_authors.setText(names)
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()