import cudf
import pandas as pd
import time

ew = cudf.read_csv('../ew_rcid_lat_lon.csv', dtype = ['category','float64','float64'])
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
df = ew.merge(df, on=['Lat', 'Lon'])
print(len(df))
