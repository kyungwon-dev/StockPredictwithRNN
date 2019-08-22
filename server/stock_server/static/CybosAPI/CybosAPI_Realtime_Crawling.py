import win32com.client
import pandas as pd
import os
import sys
import time
import datetime
import csv
import json

class CpMarketEye:
    def __init__(self,info):
        self.info = info
        self.code = list(info.values())
        self.stock = list(info.keys())
        
        self.result = os.listdir("../data/")
        self.result = [i for i in self.result if "todayStock"in i]
        
        if not self.result:
            self.result = {}
            for i in range(10):
                self.result["%s" % (self.code[i])] = []
                self.result["%s" % (self.code[i])].append({"STOCK_DATE":[]})
                self.result["%s" % (self.code[i])].append({"STOCK_PRICE":[]})
                self.result["%s" % (self.code[i])].append({"STOCK_VOLUME":[]})
                self.result["%s" % (self.code[i])].append({"RNN_PRICE":[]})
                self.result["%s" % (self.code[i])].append({"DNN_PRICE":[]})
        else:
             with open('../data/%s' % "".join(self.result)) as data_file:    
                self.result = json.load(data_file)

    def Request(self,currentDate,currentDateTime):
        # 연결 여부 체크
        objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        bConnect = objCpCybos.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            return False
        
        request_Field = [4,10]
        
        # 관심종목 객체 구하기
        objRq = win32com.client.Dispatch("CpSysDib.MarketEye")
        
        # 요청 필드 세팅 - 종목코드, 종목명, 시간, 대비부호, 대비, 현재가, 거래량
        # rqField = [0,17, 1,2,3,4,10]
        objRq.SetInputValue(0, request_Field) # 요청 필드
        objRq.SetInputValue(1, self.code)  # 종목코드 or 종목코드 리스트
        objRq.BlockRequest()
 
        # 현재가 통신 및 통신 에러 처리
        rqStatus = objRq.GetDibStatus()
        rqRet = objRq.GetDibMsg1()
        print("통신상태", rqStatus, rqRet)
        if rqStatus != 0:
            return False
 
        cnt  = objRq.GetHeaderValue(2)
        

        for i in range(cnt):
            self.result["%s" % (self.code[i])][0]["STOCK_DATE"].append(str(currentDate)+" "+str(currentDateTime))
            self.result["%s" % (self.code[i])][1]["STOCK_PRICE"].append(str(objRq.GetDataValue(0,i)))
            self.result["%s" % (self.code[i])][2]["STOCK_VOLUME"].append(str(objRq.GetDataValue(1,i)))
        return self.result
    
def setStock(stock,datapath):
    
    """
    종목코드 설정하고 (stock)
    해당 경로 설정(datapath)
    이후 csv 가져와서 찾기
    """
    filepath = os.listdir(datapath)
    csv_file = [idx for idx in filepath if 'securities' in idx]
    print("loading csv file : ",csv_file)
    securities_csv = pd.DataFrame.from_csv("%s%s" % (datapath,"".join(csv_file)), encoding='CP949', index_col=0 , header=0)
    securities_csv = securities_csv.drop_duplicates(["종목명"])
    securities_codes = {}
    for i in stock:
        securities_codes[i] = "A" + "".join(list(securities_csv[securities_csv["종목명"] == i]["종목코드"]))
    print("securities_code : ",securities_codes)
    
    return securities_codes
    
def json_save(datapath,result):
    with open("%s%s.json" % (datapath,"todayStock") , "w", encoding="utf-8") as file:
        json.dump(result, file ,ensure_ascii=False, indent="\t")            
    return None

if __name__=="__main__":
    """
    KOSPI 제약종목 10개 
    유한양행
    녹십자
    광동제약
    대웅제약
    한미약품
    종근당
    동아쏘시오홀딩스
    JW홀딩스
    제일약품
    한미사이언스
    """
    print(win32com.client.sys.version)
    stock = ["유한양행","녹십자","광동제약","대웅제약","한미약품",
                "종근당","동아쏘시오홀딩스","JW홀딩스","일동제약","한미사이언스"]
    datapath = "../data/"
    objMarkeyeye = CpMarketEye(setStock(stock,datapath))
    while True:
        now = datetime.datetime.now()
        nowDate = now.strftime("%Y%m%d")
        nowDatetime = now.strftime("%H%M") ##현재시간 구하기
        if(nowDatetime >= '0900' and nowDatetime <= '1530'): #이 시간 사이에 실행
            result = objMarkeyeye.Request(str(nowDate),str(nowDatetime))
            if result!= False:
                json_save(datapath,result)
                print("Saved..wait 60 sec")
                time.sleep(60)
            else:
                continue






