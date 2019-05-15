import cudf
import pandas as pd
import time
import numpy as np

ew = cudf.read_csv('../ew_rcid_lat_lon.csv', dtype = ['category','float32','float32'])
start = time.time()
df = cudf.read_csv('/home/data/temp.csv',dtype = ['float32','float32','float32','date'])
end = time.time()
print(end-start)
print(len(df))
start = time.time()
df = df.query("precip > 0")
end = time.time()
print(end-start)
print(df.head(10))
start = time.time()
df = ew.merge(df, on=['Lat', 'Lon'])
end = time.time()
print(end-start)
print(len(df))
df = df.drop(['Lat','Lon'])
df.add_column('Freq',np.ones(len(df)))
df = df[['RCID','precip','Freq']].groupby(by=['RCID','precip']).sum()
