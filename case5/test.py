#!/usr/bin/env python3
import os
import pandas as pd
from datetime import datetime
import cudf
from cudf.utils import cudautils
from numba import cuda
import numba
import time
import numpy as np
from joblib import Parallel ,delayed
import sys

def dropna(df, axis="index", how="all"):
        def get_is_na_mask(obj):
            return cudautils.is_na_mask(data=obj.data.to_gpu_array(),
                                        mask=obj.mask.to_gpu_array())


        if axis==0 or axis=="index":


 
            gathermask = None


 
            for k, c in df._cols.items():


 
                if gathermask is None:


 
                    gathermask = get_is_na_mask(df[k])


 
                else:


 
                    if how=="all":


 
                        gathermask = cudautils.elem_and_or(


 
                            gathermask, get_is_na_mask(df[k]), "and")


 
                    elif how=="any":

                        gathermask = cudautils.elem_and_or(
                            gathermask, get_is_na_mask(df[k]), "or")
                value = np.random.randn(0,0).astype(c._data.dtype)
                c.fillna(value)
            return df[gathermask]
        elif axis==1 or axis=="column":
            columns = []
            for k, c in df._cols.items():
                null_count = c.null_count
                if how=="all" and null_count==len(c):
                    columns.append(c.name)
                elif how=="any" and null_count>0:
                    columns.append(c.name)
            return df.drop(columns)



df = cudf.DataFrame([('Precipitation (mm)', list(range(20))),
('b', list(reversed(range(20)))),
('c', [np.nan]*18+[1,1])])
print(dropna(df))