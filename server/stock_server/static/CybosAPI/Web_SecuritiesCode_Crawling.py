import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time

import numpy as np

def get_request_url(url, enc='UTF-8'):
    
    req = urllib.request.Request(url)
    try: 
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            try:
                rcv = response.read()
                ret = rcv.decode(enc)
            except UnicodeDecodeError:
                ret = rcv.decode(enc, 'replace')    
            
            return ret
            
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None
    
def get_securities_Code(url):
    print(url)
    rcv_data = get_request_url(url)
    soupData = BeautifulSoup(rcv_data,'html.parser')
    table_tag = soupData.find('table')
    #print(table_tag)
    
    data = []
    
    for tr in table_tag.findAll("tr"):
        stock = []
        #print(tr)
        for td in tr.findAll("td"):
            stock.append(td.string)
            if(str(td.string) == "INDEX"):
                stock = []
                break
        data.append(stock)
        del(stock)
        #print(data)
    
    return data

def main():
    securities_URL = "http://bigdata-trader.com"
    securities_type = "itemcodehelp2.jsp"
    
    securities_URL = securities_URL + "/" + securities_type
    code_column = ("종목코드","종목명","종류")
    #print(securities_URL)
    
    result = get_securities_Code(securities_URL)
    
    securities_table = pd.DataFrame(result,columns=code_column)
    securities_table.to_csv("../data/securities_%s.csv" % (datetime.datetime.now().strftime("%Y%m%d")),
                            encoding="CP949",mode = 'w', index = True)
    
    print('FINISHED')
    
if __name__ == '__main__':
     main()