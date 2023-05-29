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
        uic.loadUi('PySQLite_Designer_1.ui', self)
        self.table = self.tableView
         
        database = r'C:\Users\user\Downloads\SQL\database.sqlite'
        # create a database connect
        self.conn = create_connection(database)
        with self.conn: # with can handle the exceptions, like resources released, cleaning...
            select_table(self, "Authors")

        # Signals
        self.select_table.currentIndexChanged.connect(self.queryTable)
        self.pBut_exit.clicked.connect(self.appEXIT)

    # Slots
    def queryTable(self,i):
        tbname = self.select_table.currentText()
        select_table(self, tbname)

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
 
def select_table(self, tbname):
    sql = "select * from " + tbname
    SQLExecute(self, sql)
     
def SQLExecute(self, SQL):
    """
    Execute a SQL command and display the requested items on the QTableView
    :param conn: SQL command
    :return: None
    """
    cur = self.conn.cursor()
    cur.execute(SQL)
    rows = cur.fetchall()
    if len(rows) == 0: # nothing found
        # raise a messageBox here
        dlg = QMessageBox(self)
        dlg.setWindowTitle("SQL Information: ")
        dlg.setText("Nothing Found !!!")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
        buttonY = dlg.button(QMessageBox.StandardButton.Yes)
        buttonY.setText('OK')
        dlg.setIcon(QMessageBox.Icon.Information)
        button = dlg.exec()
        return
     
    # Process fetched output
    names = [description[0] for description in cur.description]# extract column names
    self.df = pd.DataFrame(rows)
    self.model = TableModel(self.df)
    self.table.setModel(self.model)
    self.df.columns = names
    self.table.resizeColumnToContents(0) # resize the width of the 1st column
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
 
if __name__ == '__main__':
    main()