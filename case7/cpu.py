import cudf
import pandas as pd
import time

ew = pd.read_csv('../ew_rcid_lat_lon.csv')
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
df = ew.merge(df, on=['Lat', 'Lon'])
print(len(df))