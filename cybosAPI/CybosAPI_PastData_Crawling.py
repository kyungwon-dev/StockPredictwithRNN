import sys
import win32com.client
import pandas as pd
import os
import ctypes
import time
import datetime

class CpStockChart:
    def __init__(self):
        self.objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
        self.g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        self.g_objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
        
    # PLUS 실행 기본 체크 함수
    def InitPlusCheck(self,g_objCpStatus):
        # 프로세스가 관리자 권한으로 실행 여부
        if ctypes.windll.shell32.IsUserAnAdmin():
            print('정상: 관리자권한으로 실행된 프로세스입니다.')
        else:
            print('오류: 일반권한으로 실행됨. 관리자 권한으로 실행해 주세요')
            return False

        # 연결 여부 체크
        if (g_objCpStatus.IsConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            return False

        # # 주문 관련 초기화
        # if (g_objCpTrade.TradeInit(0) != 0):
        #     print("주문 초기화 실패")
        #     return False

        return True
    
    # 차트 요청 - 기간 기준으로
    def RequestFromTo(self, code, dwm,fromDate, toDate, caller):
        print(code, fromDate, toDate)
        # 연결 여부 체크
        if self.InitPlusCheck(self.g_objCpStatus) == False:
            return False
 
        self.objStockChart.SetInputValue(0, code)  # 종목코드
        self.objStockChart.SetInputValue(1, ord('1'))  # 기간으로 받기
        self.objStockChart.SetInputValue(2, toDate)  # To 날짜
        self.objStockChart.SetInputValue(3, fromDate)  # From 날짜
        self.objStockChart.SetInputValue(5, [0, 1, 2, 8])  # 날짜,시간,시가,거래량
        self.objStockChart.SetInputValue(6, dwm)  # '차트 주기 - 분/틱
        self.objStockChart.SetInputValue(7, 1)  # 분틱차트 주기
        self.objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용
        self.objStockChart.BlockRequest()
 
        rqStatus = self.objStockChart.GetDibStatus()
        rqRet = self.objStockChart.GetDibMsg1()
        print("통신상태", rqStatus, rqRet)
        if rqStatus != 0:
            exit()
 
        len = self.objStockChart.GetHeaderValue(3)
 
        caller.dates = []
        caller.opens = []
        caller.vols = []
        caller.times = []
        for i in range(len):
            caller.dates.append(self.objStockChart.GetDataValue(0, i))
            caller.times.append(self.objStockChart.GetDataValue(1, i))
            caller.opens.append(self.objStockChart.GetDataValue(2, i))
            caller.vols.append(self.objStockChart.GetDataValue(3, i))
 
        return 

class PastStock:
    def __init__(self):
        
        self.dates = []
        self.opens = []
        self.vols = []
        self.times = []
 
        self.objChart = CpStockChart()
        
        self.stock_list = ["유한양행","녹십자","광동제약","대웅제약","한미약품",
                "종근당","동아쏘시오홀딩스","JW홀딩스","일동제약","한미사이언스"]
        self.datapath = "../data/"
        self.init_stock = self.setStock(self.stock_list,self.datapath)
        self.stock_code = tuple(self.init_stock.values())
 
 
    def setStock(self,stock,datapath):
    
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

    def save_Stock(self,toDate,fromDate):
        for i in range(len(self.stock_code)):
            self.dates = []
            self.opens = []
            self.vols = []
            self.times = []
            self.objChart.RequestFromTo(self.stock_code[i],ord('m'),toDate,fromDate,self )
            self.dates.reverse()
            self.times.reverse()
            self.opens.reverse()
            self.vols.reverse()
            chartData = {
                '일자' : self.dates,
                '시간' : self.times,
                '현재가' : self.opens,
                '거래량' : self.vols,
            }
            df = pd.DataFrame(chartData, columns=['일자','시간','현재가','거래량'])
            
            if toDate == "20180101":   
                df.to_csv("%s%s_%s.csv" % (self.datapath,self.stock_code[i],self.stock_list[i]), header = True, encoding="CP949")
            else:
                df.to_csv("%s%s_%s.csv" % (self.datapath,self.stock_code[i],self.stock_list[i]), mode='a', header = False, encoding="CP949")
        time.sleep(60)
        return 

if __name__=="__main__":
    print(sys.version)
    start = PastStock()
    now = datetime.datetime.now()
    nowDate = now.strftime("%m%d")
    timeToSave = [x for x in range(101, int(nowDate), 3) if x%100 < 32 ]
    timeToSave = [x for x in timeToSave if x%100!=0]
    timeToSave = [x for x in timeToSave if x!=230]
    for i in range(len(timeToSave)-1):
        start.save_Stock(str(20180000+int(timeToSave[i])),str(20180000+int(timeToSave[i+1])-1))
    
