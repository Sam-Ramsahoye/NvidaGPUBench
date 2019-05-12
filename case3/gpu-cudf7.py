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
def file_read(path,file,ew_gpu):
    cudfObj = cudf.read_csv(path+file).drop(['Date','Time'])
    return ew_gpu.merge(cudfObj, on=['Lat', 'Lon'])

# Getting ID-Location Association
ew_gpu = cudf.read_csv('../ew_rcid_lat_lon.csv', dtype = ['category','float64','float64'])

path = '../../data/'
year = '2014'
files = os.listdir(path)
filesRequired = [f for f in files if 'nr' in f]

nProc = 16
nFilesArr = [1, 10, 100, 1000]
nFilesArr = [i*nProc for i in nFilesArr]
dfSizeArr = []
tArr = []

for nFiles in nFilesArr:
    start = time.time()
    out = Parallel(n_jobs = nProc)(delayed(file_read)(path,f,ew_gpu) for f in filesRequired[:nFiles])
    df = cudf.concat(out)
    end = time.time()
    print(end-start)
    tArr.append(end-start)
    dfSizeArr.append(sys.getsizeof(df))
    del out

print(tArr)
print(dfSizeArr)


