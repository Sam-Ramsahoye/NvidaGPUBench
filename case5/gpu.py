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

# Filter Precipitation
@cuda.jit
def filter_precipitation(in_arr_1, out_arr, arr_len):

    i = cuda.grid(1)

    if i < arr_len:
        if in_arr_1[i] < 0:
            out_arr[i] = np.nan

# Getting ID-Location Association
ew_gpu = cudf.read_csv('../ew_rcid_lat_lon.csv', dtype = ['category','float64','float64'])

path = '../../data/'
files = os.listdir(path)
filesRequired = [f for f in files if 'nr' in f]

nProc = 16
nFilesArr = [1]
nFilesArr = [i*nProc for i in nFilesArr]
dfSizeArr = []
tArr = []

for nFiles in nFilesArr:
    # Reading Data and Concatenation Files
    start = time.time()
    out = Parallel(n_jobs = nProc)(delayed(file_read)(path,f,ew_gpu) for f in filesRequired[:nFiles])
    df = cudf.concat(out)
    end = time.time()
    print(end-start)
    tArr.append(end-start)
    dfSizeArr.append(sys.getsizeof(df))
    del out
    
    # Filtering Precipitation
    nRows = len(df)
    gpu_in_4 = df['Precipitation (mm)'].to_gpu_array()
    gpu_out_4 = np.zeros(nRows)
    number_of_threads = 128
    number_of_blocks = (nRows + (number_of_threads-1)) // number_of_threads

    # Caching Function
    filter_precipitation[(number_of_blocks,), (number_of_threads, )](gpu_in_4,gpu_out_4,nRows)
    cuda.synchronize()

    filter_precipitation[(number_of_blocks,), (number_of_threads, )](gpu_in_4,gpu_out_4,nRows)
    cuda.synchronize()

    df_pd = cudf.to_pandas()
    df_pd.to_csv('test.csv')
    #df = df.iloc[list(np.where(gpu_out_4 == 0)[0])]





