import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox 
from PyQt6.QtCore import Qt
import pandas as pd
import sqlite3
from sqlite3 import Error
 
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
        uic.loadUi('SQL_key_in_code.ui', self)
        self.table = self.tableView
        self.page = 1
        self.one_page_rows = 100
         
        database = r'C:\Users\user\Downloads\SQL\database.sqlite'
        # create a database connect
        self.conn = create_connection(database)

        # Singals
        self.lineEdit.returnPressed.connect(self.update_data)
        self.pBut_exit.clicked.connect(self.appEXIT)
        self.pBut_first.clicked.connect(self.show_first)
        self.pBut_previous.clicked.connect(self.show_previous)
        self.pBut_next.clicked.connect(self.show_next)
        self.pBut_last.clicked.connect(self.show_last)
        self.cBox.currentIndexChanged.connect(self.set_page)

    def update_data(self):
        tb = str(self.lineEdit.text())
        update_table(self, tb)
        # self.cBox.addItems(str(i) for i in range(1, self.total_page))

    def show_first(self):
        self.page = 1
        change_page(self)
    
    def show_previous(self):
        if self.page > 1:
            self.page -= 1
            change_page(self)
        else:
            pass
    
    def show_next(self):
        self.page += 1
        change_page(self)

    def show_last(self):
        self.page = 'last_page'
        change_page(self)

    def set_page(self):
        self.page = int(self.cBox.currentText())
        change_page(self)

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

def update_table(self, sql):
    SQLExecute(self, sql)

def SQLExecute(self, SQL):
    """
    Execute a SQL command and display the requested items on the QTableView
    :param conn: SQL command
    :return: None
    """
    self.cur = self.conn.cursor()
    try:
        self.cur.execute(SQL)
    except Error as e:
        display_message(str(e))
        return None
    rows = self.cur.fetchall()
    self.df = pd.DataFrame(rows)
    change_page(self)
    self.cBox.addItems(str(i) for i in range(1, (len(self.df)//self.one_page_rows) + 2))

def display_message(message):
    dlg = QMessageBox()
    dlg.setWindowTitle("SQL Information: ")
    dlg.setText(message)
    dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
    buttonY = dlg.button(QMessageBox.StandardButton.Yes)
    buttonY.setText('OK')
    dlg.setIcon(QMessageBox.Icon.Information)
    dlg.exec()

def change_page(self):
    # Process fetched output
    names = [description[0] for description in self.cur.description]
    if self.page == 'last_page':
        self.dff = pd.DataFrame(self.df[(len(self.df)//self.one_page_rows)*self.one_page_rows:len(self.df)])
        self.model = TableModel(self.dff)
        self.table.setModel(self.model)
        self.dff.columns = names
        self.table.resizeColumnToContents(0)
        self.page = len(self.df)//self.one_page_rows + 1
        self.label_page.setText(str(len(self.df)//self.one_page_rows + 1))
    
    elif 1 <= self.page <= (len(self.df)//self.one_page_rows) + 1:
        self.dff = pd.DataFrame(self.df[(self.page-1) * self.one_page_rows : self.page * self.one_page_rows])
        self.model = TableModel(self.dff)
        self.table.setModel(self.model)
        self.dff.columns = names
        self.table.resizeColumnToContents(0)
        self.label_page.setText(str(self.page))
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()