# SELECT data from a table
 
import sqlite3
from sqlite3 import Error
 
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
 
def select_table(conn, tbname):
    """
    Query table data
    :param conn: the Connection object
    :param tbname: table name
    :return:
    """
    cur = conn.cursor()
    sql = "select * from " + tbname
    cur.execute(sql)
    rows = cur.fetchall()
 
    for row in rows[0:10]:
        print(row)
 
def main():
    database = r"C:\Users\user\Downloads\SQL\database.sqlite"
 
    # create a database connection
    conn = create_connection(database)
    with conn: # with can take care conn.close()
        print("Connection successful")
        select_table(conn, "paperauthors") # authors, papers
        count_eventtype(conn)
     
    # with create_connection(database) as conn:
    #     print("Connection successful")
    #     select_table(conn, "paperauthors") # authors, papers

def count_eventtype(conn):
    """
    論文有哪幾種型態(eventtype)?各有幾篇?
    """
    cur = conn.cursor()
    sql = "select distinct eventtype from papers"
    cur.execute(sql)
    rows = cur.fetchall()
    sql = "select count(*) from papers where eventtype = ?"
     
    for i in range(len(rows)):
        cur.execute(sql, rows[i])
        cnt = cur.fetchall()
        print(rows[i][0] + ":" + str(cnt[0][0]))
 
if __name__ == '__main__':
    main()