#!/usr/bin/env python3
import os
import pandas as pd
from datetime import datetime
import cudf
from numba import cuda
import numba
import time
import numpy as np
from joblib import Parallel ,delayed
import sys

# fileRead
def file_read(path,file):
    cudfObj = cudf.read_csv(path+file).drop(['Date','Time'])
    return cudfObj

# Getting ID-Location Association
ew_gpu = cudf.read_csv('../ew_rcid_lat_lon.csv', dtype = ['category','float64','float64'])

path = '../../data/'
files = os.listdir(path)
filesRequired = [f for f in files if 'nr' in f]

nProc = 16
nFilesArr = [300]
nFilesArr = [i*nProc for i in nFilesArr]
dfSizeArr = []
tArr = []

for nFiles in nFilesArr:
    out = Parallel(n_jobs = nProc)(delayed(file_read)(path,f) for f in filesRequired[:nFiles])
    df = cudf.concat(out)
    dfSizeArr.append(sys.getsizeof(df))
    del out
    # print(len(df))
    # start = time.time()
    # df = df.groupby(by=['RCID','Precipitation (mm)'])
    # end = time.time()
    # print(end-start)
    # tArr.append(end-start)
    

print(tArr)
print(dfSizeArr)