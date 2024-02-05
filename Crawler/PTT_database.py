import sqlite3
import mysql.connector
from mysql.connector import Error
from config import mysql_config

def transfer_data(sqlite_db_path, mysql_config):
    sqlite_conn = sqlite3.connect(sqlite_db_path)
    sqlite_cursor = sqlite_conn.cursor()
    
    try:
        mysql_conn = mysql.connector.connect(**mysql_config)
        mysql_cursor = mysql_conn.cursor()
        print("成功連接到 MySQL")
    except Error as e:
        print(f"連接到 MySQL 時出錯：{e}")
        return
    
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = sqlite_cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"處理資料表：{table_name}")

        assert table_name =='PTT' ,f'file name error'

        sqlite_cursor.execute(f"SELECT * FROM {table_name}")
        rows = sqlite_cursor.fetchall()
        columns = [description[0] for description in sqlite_cursor.description]
        column_names = ", ".join(columns)
        
        print(f"CREATE TABLE IF NOT EXISTS `ptt` (`board` VARCHAR(255), `id` VARCHAR(255), `pushes` VARCHAR(255), `author` VARCHAR(255), `title` VARCHAR(255));")
        
        mysql_cursor.execute(f"CREATE TABLE IF NOT EXISTS `ptt` (`board` VARCHAR(255), `id` VARCHAR(255), `pushes` VARCHAR(255), `author` VARCHAR(255), `title` VARCHAR(255));")
        
        # 將資料插入 MySQL 資料表
        placeholders = ", ".join(["%s"] * len(columns))
        mysql_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        mysql_cursor.executemany(mysql_query, rows)
        mysql_conn.commit()
        
        print(f"成功將資料從 SQLite 的 {table_name} 資料表轉移到 MySQL")
    
    sqlite_conn.close()
    mysql_conn.close()
    print("資料轉移完成。")


if __name__=='__main__':

    sqlite_db_path = 'mydatabase_0205.db'

    transfer_data(sqlite_db_path, mysql_config)
