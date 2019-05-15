import cudf
import pandas as pd
import time
#df = cudf.read_csv('temp.csv')
start = time.time()
df = pd.read_csv('/home/data/temp.csv', parse_dates = ['DateTime'])
end = time.time()
print(end-start)
print(len(df))
start = time.time()
df = df[df['precip'] > 0]
end = time.time()
print(end-start)
print(df.head(10))
