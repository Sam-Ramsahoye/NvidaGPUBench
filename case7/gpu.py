import cudf
import pandas as pd
import time
#df = cudf.read_csv('temp.csv')
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
