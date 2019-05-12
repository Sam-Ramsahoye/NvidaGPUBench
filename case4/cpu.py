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
    pdObj = pd.read_csv(path+file)
    return pdObj

path = '../../data/'
year = '2014'
files = os.listdir(path)
filesRequired = [f for f in files if 'nr' in f]

nProc = 16
nFilesArr = [10]
nFilesArr = [i*nProc for i in nFilesArr]
tArrCPU = []
tArrGPU = []

for nFiles in nFilesArr:
    out = Parallel(n_jobs = nProc)(delayed(file_read)(path,f) for f in filesRequired[:nFiles])
    df = pd.concat(out)
    df.to_csv('temp.csv', index = False)

    start = time.time()
    pd = pd.read_csv('temp.csv')
    end = time.time()
    tArrCPU.append(end-start)
    print(end-start)
    del pd

    start = time.time()
    pd = cudf.read_csv('temp.csv')
    end = time.time()
    tArrGPU.append(end-start)
    print(end-start) 
    del pd

    del out
    del df
    os.remove('temp.csv')


print(tArrCPU)
print(tArrGPU)
