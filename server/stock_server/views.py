from django.shortcuts import render
from django.shortcuts import render, HttpResponse, render_to_response

import random, json
import ctypes , os
import pandas as pd
import numpy as np
import threading,subprocess

def data_page(request):
    return render_to_response('Stock_Data.html')

def model_page(request):
    return render_to_response('Stock_Data.html')

def chart_page(request):
    
    #jsondata = addLearningData()
    print(os.getcwd())
    datadir = os.listdir("./stock_server/static/data/")
    datadir = [i for i in datadir if 'A'in i]
    codelist = [i[:7] for i in datadir ]
    namelist = [i[8:-4] for i in datadir]
    codename = [i[:-4] for i in datadir]
    
    temp = {
        'codename':codename,
        'codelist':codelist,
        'namelist':namelist,
    }
    return render(request, 'Stock_Chart.html', temp)    
