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

# hashing time
def time_conv(x):
    #print(type(x))
    #print(x)
    temp = x.split(' ')

    ymd = temp[0].split('-')
    hm = temp[1].split(':')
    return datetime(int(ymd[0]),int(ymd[1]),int(ymd[2]),int(hm[0]),int(hm[1]),0).timestamp()

# hasting id
def id_conv(x):
    temp = x.split('RC')
    return int(temp[1])

# fileRead
def file_read(path,file,ew):
    pdObj = pd.read_csv(path+file).drop(['Date','Time'], axis = 1).dropna()
    pdObj['DateTime'] = pdObj['DateTime'].apply(time_conv)
    pdObj = pdObj[pdObj['Precipitation (mm)'] >= 0]
    return cudf.from_pandas(pdObj.merge(ew, on=['Lat', 'Lon']))

# Getting Required Data
ew = pd.read_csv('ew_rcid_lat_lon.csv')
ew['RCID'] = ew['RCID'].apply(id_conv)

df_cu = cudf.read_csv(path+filesRequired[10,names = ['Lat','Lon','Precipitation (mm)','DateTime'],dtype = ['float','float','float','str'])
print(df_cu.head())

# nTimes = 500
# totalTime = 0.0
# path = '../data/'
# yearMonth1 = '201401'
# files = os.listdir(path)
# filesRequired = [f for f in files if (yearMonth1 in f)]
# df_pd = pd.read_csv(path+filesRequired[1])
# print(df_pd.head())
# print(len(df_pd))
# out = Parallel(n_jobs = 16)(delayed(file_read)(path,f,ew) for f in filesRequired[0:nTimes])
# df_original_gpu = cudf.concat(out)
# end = time.time()
