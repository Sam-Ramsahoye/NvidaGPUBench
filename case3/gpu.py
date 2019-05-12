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
    return cudfObj.merge(ew_gpu, on=['Lat', 'Lon'])

# hasting id
def id_conv(x):
    temp = x.split('RC')
    return int(temp[1])

# Getting Required Data
ew = pd.read_csv('../ew_rcid_lat_lon.csv')
ew['RCID'] = ew['RCID'].apply(id_conv)
ew_gpu = cudf.from_pandas(ew)

path = '../../data/'
year = '2014'
files = os.listdir(path)

filesRequired = [f for f in files if (year in f)]
nProc = 16
nFilesArr = [75]
nFilesArr = [i*nProc for i in nFilesArr]
tArr = []
for nFiles in nFilesArr:
    start = time.time()
    #out = Parallel(n_jobs = nProc)(delayed(file_read)(path,f) for f in filesRequired[:nFiles])
    df = cudf.concat(Parallel(n_jobs = nProc)(delayed(file_read)(path,f,ew_gpu) for f in filesRequired[100:1400]))
    end = time.time()
    print(end-start)
    tArr.append(end-start)
    del out

print(sys.getsizeof(df))
#print(tArr)


