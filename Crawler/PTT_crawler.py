import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl
import sqlite3
import numpy as np
from datetime import datetime
import argparse

class Datetimeclass:
    def __init__(self) -> None:
        self.now = datetime.now()
        pass
    def today_format(self,format='%m%d'):
        return self.now.strftime(format)

class DatabaseHandler:
    def __init__(self, db_name):
        self.db_file = db_name
        self.conn = None

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
        except:
            print("Connection error")

    def create_table(self, create_table_query):
        try:
            c = self.conn.cursor()
            c.execute(create_table_query)
            # self.conn.commit()  # Uncomment this line if you want to commit changes immediately
        except:
            print("Create table error")

    def add_new_row(self, insert_list):
        # Insert new data
        try:
            cursor = self.conn.cursor()
            str_insert_list = "'" + "','".join(insert_list) + "'"
            add_new_row_query = f"""INSERT INTO PTT(board, id, pushes, author, title)
                                   VALUES({str_insert_list})"""

            cursor.execute(add_new_row_query)
            self.conn.commit()
        except:
            print('?')
            print(insert_list)
    
    def get_data(self,query):
        query_result = pd.read_sql(query,self.conn)
        return query_result

    def close_connection(self):
        if self.conn:
            self.conn.close()


def crawler(dt,numberofpage):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["看板名稱",'id',"推文數","文章作者","文章名稱"]) 
    
    for board_name in ('NBA',"Stock",'Boy-Girl','Baseball',"Lifeismoney"):
        url = 'https://www.ptt.cc/bbs/'+board_name+'/index.html'
        for page in range(1,numberofpage): #30頁
            print(url)  #當前的url
            print(board_name,"版page",page)
            time.sleep(2)
            web = requests.get(url,cookies={'over18':'1'})
            soup = BeautifulSoup(web.text, "html.parser")
            pushes = soup.find_all('div',class_='nrec')
            authors = soup.find_all('div',class_='author')
            titles = soup.find_all('div', class_='title')  
            for i,j,k in zip(titles,pushes,authors):
                if i.find('a') != None:                        
                    a = j.text
                    
                    id = i.find('a').get("href")[i.find('a').get("href").find(board_name):i.find('a').get("href").find('.A.')]
                    
                    b=0
                    
                    if a =='爆':
                        url_article = "https://www.ptt.cc"+i.find('a').get('href')
                        web_article = requests.get(url_article,cookies={'over18':'1'})
                        soup_article = BeautifulSoup(web_article.text, "html.parser")
                        b=0
                        pushnumber = soup_article.find_all('div',class_='push')
                        for m in pushnumber:
                            if m.text[0] == '推':
                                b+=1
                            elif m.text[0] == '噓':
                                b-=1
                    
                    if b>0:
                        data = [board_name,id,str(b),k.text,i.text]
                        ws.append(data)
                        handler.add_new_row(data)
                    else:
                        data = [board_name,id,a,k.text,i.text]
                        ws.append(data)
                        handler.add_new_row(data)
      

            url = "https://www.ptt.cc"+soup.find_all("a",class_='btn wide')[1].get('href') #上一頁的href


    # Close the connection when done
    wb.save(f"PPT_{dt}.xlsx")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='crawler')
    parser.add_argument('--page',type=int,required=True,default=2,help='number of page to crawl')
    args = parser.parse_args()
    numberofpage = args.page

    dt = Datetimeclass().today_format()
    database_name = f"mydatabase_{dt}.db"
    handler = DatabaseHandler(database_name)
    handler.create_connection()

    # create tables
    if handler.conn is not None:
        sql_create_ptt_table_query = f"""CREATE TABLE IF NOT EXISTS PTT (
                                    board text NOT NULL,
                                    id text,
                                    pushes text,
                                    author text,
                                    title text
                                );"""
        handler.create_table(sql_create_ptt_table_query)
    else:
        print("Error! cannot create the database connection.")

    crawler(dt,numberofpage)
    handler.close_connection()