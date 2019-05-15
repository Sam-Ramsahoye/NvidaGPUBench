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

# fileRead
def file_read(path,file):
    pdObj = pd.read_csv(path+file).drop(['Date','Time'], axis = 1)
    pdObj.rename(columns={'Precipitation (mm)': 'precip'}, inplace = True)
    return pdObj

path = '../../data/'
year = 'nr'
files = os.listdir(path)

filesRequired = [f for f in files if (year in f)]
nProc = 16
nFilesArr = [100]
nFilesArr = [i*nProc for i in nFilesArr]
tArr = []

for nFiles in nFilesArr:
    out = Parallel(n_jobs = nProc)(delayed(file_read)(path,f) for f in filesRequired[:nFiles])
    df = pd.concat(out)
    del out
    df.to_csv('temp.csv', index = False)

