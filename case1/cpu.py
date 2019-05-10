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
    pdObj = pd.read_csv(path+file)
    return pdObj

path = '../../data/'
year = '2014'
files = os.listdir(path)

filesRequired = [f for f in files if (year in f)]
nFiles = 200
start = time.time()
out = Parallel(n_jobs = 16)(delayed(file_read)(path,f) for f in filesRequired[:nFiles])
df = pd.concat(out)
end = time.time()
print(end-start)

