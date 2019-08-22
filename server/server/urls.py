"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

import stock_server.views
import time

import datetime
import os,threading,subprocess

import json
import tensorflow as tf
import numpy as np
import pandas as pd
import cx_Oracle
from sqlalchemy import types, create_engine
tf.set_random_seed(1008)

def addLearningData():
    jsondata = os.listdir("./stock_server/static/data/")
    codelist = [i[:7] for i in jsondata if 'A' in i]
    jsondata = [i for i in jsondata if 'todayStock'in i]
    with open('./stock_server/static/data/%s' % "".join(jsondata)) as today_file:
        jsondata = json.load(today_file)
            
    return jsondata
def lstm_cell(rnn_cell_hidden_dim,keep_prob,forget_bias):
    
    cell = tf.contrib.rnn.BasicLSTMCell(num_units=rnn_cell_hidden_dim, 
                                        forget_bias=forget_bias, state_is_tuple=True, activation=tf.nn.softsign)
    if keep_prob < 1.0:
        cell = tf.contrib.rnn.DropoutWrapper(cell, output_keep_prob=keep_prob)
    return cell        
def reverse_min_max_scaling(org_x, x):
    org_x_np = np.asarray(org_x)
    x_np = np.asarray(x)
    return (x_np * (org_x_np.max() - org_x_np.min() + 1e-7)) + org_x_np.min()

def min_max_scaling(x):
    x_np = np.asarray(x)
    return (x_np - x_np.min()) / (x_np.max() - x_np.min() + 1e-7) # 1e-7은 0으로 나누는 오류 예방차원

# Standardization
def data_standardization(x):
    x_np = np.asarray(x)
    return (x_np - x_np.mean()) / x_np.std()

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
        

def learning_RNN():
    while True:
        resultset = []
        
        # 하이퍼파라미터
        input_data_column_cnt = 2 # 입력데이터의 컬럼 개수(Variable 개수)
        output_data_column_cnt = 1 # 결과데이터의 컬럼 개수

        seq_length = 10            # 1개 시퀀스의 길이(시계열데이터 입력 개수)
        rnn_cell_hidden_dim = 10   # 각 셀의 (hidden)출력 크기
        forget_bias = 1.0          # 망각편향(기본값 1.0)
        num_stacked_layers = 1     # stacked LSTM layers 개수
        keep_prob = 1.0            # dropout할 때 keep할 비율

        epoch_num = 200           # 에폭 횟수(학습용전체데이터를 몇 회 반복해서 학습할 것인가 입력)
        learning_rate = 0.01       # 학습률

        datapath = os.listdir("./stock_server/static/data/")
        datapath = [i for i in datapath if 'A' in i]
        dataname = [i[:7] for i in datapath]
        print(datapath)
        print(dataname)
        # 텐서플로우 플레이스홀더 생성
        # 입력 X, 출력 Y를 생성한다
        X = tf.placeholder(tf.float32, [None, seq_length, input_data_column_cnt], name="inputData")
        Y = tf.placeholder(tf.float32, [None, 1] ,name="outputData")

        # 검증용 측정지표를 산출하기 위한 targets, predictions를 생성한다
        targets = tf.placeholder(tf.float32, [None, 1] ,name="target")
        predictions = tf.placeholder(tf.float32, [None, 1],name="predict" )
        stackedRNNs = [lstm_cell(rnn_cell_hidden_dim,keep_prob,forget_bias) for _ in range(num_stacked_layers)]
        multi_cells = tf.contrib.rnn.MultiRNNCell(stackedRNNs, state_is_tuple=True) if num_stacked_layers > 1 else lstm_cell(rnn_cell_hidden_dim,keep_prob,forget_bias)

        # RNN Cell(여기서는 LSTM셀임)들을 연결
        hypothesis, _states = tf.nn.dynamic_rnn(multi_cells, X, dtype=tf.float32)
        hypothesis = tf.contrib.layers.fully_connected(hypothesis[:, -1], output_data_column_cnt, activation_fn=tf.identity )

        # 손실함수로 평균제곱오차를 사용한다
        loss = tf.reduce_sum(tf.square(hypothesis - Y))
        # 최적화함수로 AdamOptimizer를 사용한다
        optimizer = tf.train.AdamOptimizer(learning_rate)
        train = optimizer.minimize(loss)

        train_error_summary = [] # 학습용 데이터의 오류를 중간 중간 기록한다
        test_error_summary = []  # 테스트용 데이터의 오류를 중간 중간 기록한다
        test_predict = ''        # 테스트용데이터로 예측한 결과

        sess = tf.Session()
        sess.run(tf.global_variables_initializer())
    
        todayTemp = addLearningData()
        start_time = datetime.datetime.now() # 시작시간을 기록한다
        print(start_time)
        for i in range(len(dataname)):
            # 데이터를 로딩한다.
            connect = cx_Oracle.connect("STOCKDJANGO", "dhruddnjs", "localhost/orcl")
            target_DataFrame = read_query(connect,"select * from %s" % dataname[i])
            target_DataFrame = target_DataFrame.set_index("STOCK_INDEX")
            target_DataFrame = target_DataFrame.sort_index()

            del target_DataFrame['STOCK_DATE'] # 위 줄과 같은 효과
            del target_DataFrame['STOCK_TIME'] # 위 줄과 같은 효과
            
            temp_len = len(todayTemp[dataname[i]][1]["STOCK_PRICE"])
            target_DataFrame = target_DataFrame.tail(800-temp_len)
            
            
            stock_info = target_DataFrame.values[0:].astype(np.float) # 금액&거래량 문자열을 부동소수점형으로 변환한다
            
            price = stock_info[:,:-1]
            npp = np.array([todayTemp[dataname[i]][1]["STOCK_PRICE"]],dtype="float")
            price = np.concatenate((price,npp.T),axis=0)
            norm_price = min_max_scaling(price) # 가격형태 데이터 정규화 처리
            
            volume = stock_info[:,-1:]

            npp = np.array([todayTemp[dataname[i]][2]["STOCK_VOLUME"]],dtype="float")

            volume = np.concatenate((volume,npp.T),axis=0)
            norm_volume = min_max_scaling(volume) # 거래량형태 데이터 정규화 처리

            
            x = np.concatenate((norm_price, norm_volume), axis=1) # axis=1, 세로로 합친다
            y = x[:, [0]] # 타켓은 주식 현재가 이다.
            dataX = [] # 입력으로 사용될 Sequence Data
            dataY = [] # 출력(타켓)으로 사용

            for i in range(0, len(y) - seq_length):
                _x = x[i : i+seq_length]
                _y = y[i + seq_length] # 다음 나타날 주가(정답)
                dataX.append(_x) # dataX 리스트에 추가
                dataY.append(_y) # dataY 리스트에 추가

            # 학습용/테스트용 데이터 생성
            # 전체 70%를 학습용 데이터로 사용
            train_size = int(len(dataY) * 0.7)
            # 나머지(30%)를 테스트용 데이터로 사용
            test_size = len(dataY) - train_size

            # 데이터를 잘라 학습용 데이터 생성
            trainX = np.array(dataX[0:train_size])
            trainY = np.array(dataY[0:train_size])

            # 데이터를 잘라 테스트용 데이터 생성
            testX = np.array(dataX[train_size:len(dataX)])
            testY = np.array(dataY[train_size:len(dataY)])

            
            print('학습을 시작합니다...')
            for epoch in range(epoch_num):
                _, _loss = sess.run([train, loss], feed_dict={X: trainX, Y: trainY})

            recent_data = np.array([x[len(x)-seq_length : ]])
            # 내일 종가를 예측해본다
            test_predict = sess.run(hypothesis, feed_dict={X: recent_data})
            test_predict = reverse_min_max_scaling(price,test_predict)
            resultset.append(str(round(float(test_predict[0]))))
            print(test_predict[0])
        end_time = datetime.datetime.now() # 종료시간을 기록한다
        #elapsed_time = end_time - start_time # 경과시간을 구한다
        print(end_time)
        for i in range(len(dataname)):
            todayTemp[dataname[i]][3]["RNN_PRICE"].append(resultset[i])
        tf.reset_default_graph()
        with open("%s%s.json" % ('./stock_server/static/data/',"todayStock") , "w", encoding="utf-8") as file:
            json.dump(todayTemp, file ,ensure_ascii=False, indent="\t")

t = threading.Thread(target=learning_RNN)
t.start()
    

urlpatterns = [
    #url(r'^admin', include(admin.site.urls)),
    url(r'^admin', admin.site.urls),
    url(r'^$', stock_server.views.chart_page),
    url(r'^stock_data$', stock_server.views.data_page),
]