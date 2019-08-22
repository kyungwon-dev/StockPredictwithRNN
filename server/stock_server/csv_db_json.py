import cx_Oracle
import pandas as pd
import os
from sqlalchemy import types, create_engine
import json
import time
import datetime

def read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute( query )
        names = [ x[0] for x in cursor.description]
        rows = cursor.fetchall()
        return pd.DataFrame( rows, columns=names)
    finally:
        if cursor is not None:
            cursor.close()

def json_save(datapath,result):
    with open("%s%s.json" % (datapath,"pastStock") , "w", encoding="utf-8") as file:
        json.dump(result, file ,ensure_ascii=False, indent="\t")            
    return None

def csv_to_orclDB(codelist,datadir,conn):
    for i in range(len(codelist)):
    
        # Table Create Query
        # 이미 생성되어 있다면 , 실행하지 말아야 함.
        
        createQuery = """
        CREATE TABLE %s 
        (
          STOCK_INDEX INTEGER NOT NULL 
        , STOCK_DATE INTEGER 
        , STOCK_TIME INTEGER 
        , STOCK_PRICE INTEGER 
        , STOCK_VOLUME INTEGER 
        , CONSTRAINT %s_PK PRIMARY KEY 
          (
            STOCK_INDEX 
          )
          ENABLE 
        )""" % (codelist[i],codelist[i])

        cursor = connect.cursor() # cursor 객체 얻어오기
        cursor.execute(createQuery)
    
        connect.commit()
    
        df = pd.read_csv('./static/data/%s' % datadir[i], engine='python',encoding='cp949',index_col=0,error_bad_lines=False)
        df = df.reset_index(drop=True)
        df = df.reset_index(level=0)

        df.columns = ["STOCK_INDEX","STOCK_DATE","STOCK_TIME","STOCK_PRICE","STOCK_VOLUME"]
        df = df.set_index("STOCK_INDEX")
        df = df.sort_index()

        df.to_sql('%s' % codelist[i].lower(), conn, if_exists='append')
        
        print("%s.db Connection Seccess" % codelist[i])
        
def orclDB_to_json(codelist):
    #pastdata.json 생성 파일
    result_dict = {}
    
    for i in codelist:
        result_dict[i] = []
        df = read_query(connect,"select * from %s" % i)

        date = df["STOCK_DATE"].unique().tolist()
        date.sort()
    
        for j in date:
            target = df[df['STOCK_DATE']==j]

            target = target["STOCK_PRICE"]
            target = target.reset_index(drop=True)

            date_string = datetime.datetime.strptime(str(j)+"1530", '%Y%m%d%H%M')
            timestamp = int(time.mktime(date_string.timetuple()))*1000
            max = int(target.max())
            min = int(target.min())
            start = int(target[0])
            end = int(list(target)[-1])

            result_dict[i].append([timestamp,start,max,min,end])
    
    datapath = "./static/data/"
    json_save(datapath,result_dict)

if __name__=="__main__":
    datadir = os.listdir("./static/data/")
    datadir = [i for i in datadir if 'A'in i]
    codelist = [i[:7] for i in datadir ]
    namelist = [i[8:-4] for i in datadir]
    connect = cx_Oracle.connect("STOCKDJANGO", "dhruddnjs", "localhost/orcl")
    conn = create_engine('oracle+cx_oracle://STOCKDJANGO:dhruddnjs@localhost:1521/?service_name=orcl')
    print(codelist)
    print(namelist)
    print(datadir)
    csv_to_orclDB(codelist,datadir,conn)
    orclDB_to_json(codelist)