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
    #cudfObj = cudf.read_csv(path+file, names=['Lat','Lon','Precipitation','DateTime'],dtype = ['float64','float64','float64','date'], skiprows = 1)
    cudfObj = cudf.read_csv(path+file).drop(['Date','Time'])
    print(type(cudfObj['Lat'][0]))
    print(type(cudfObj['Lon'][0]))
    print(cudfObj)
    return ew_gpu.merge(cudfObj, on=['Lat', 'Lon'])

# hasting id
def id_conv(x):
    temp = x.split('RC')
    return int(temp[1])

# Getting Required Data
ew_gpu = cudf.read_csv('../ew_rcid_lat_lon.csv', dtype = ['category','float64','float64'])
#ew['RCID'] = ew['RCID'].apply(id_conv)
#print(ew.head())
#ew_gpu = cudf.from_pandas(ew)
print(type(ew_gpu['RCID'][0]))
print(type(ew_gpu['Lat'][0]))
print(type(ew_gpu['Lon'][0]))
print(ew_gpu)
path = '../../data/'
year = '2014'
files = os.listdir(path)

filesRequired = [f for f in files if (year in f)]
nProc = 16
nFilesArr = [75]
nFilesArr = [i*nProc for i in nFilesArr]
#df = cudf.concat(Parallel(n_jobs = nProc)(delayed(file_read)(path,f,ew_gpu) for f in filesRequired[:16]))
print(filesRequired[0])
print(filesRequired[1])
df = cudf.concat([file_read(path,f,ew_gpu) for f in filesRequired[0:2]])

print(sys.getsizeof(df))
#print(tArr)


