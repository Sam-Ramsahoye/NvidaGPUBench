import cudf
import pandas as pd
#df = cudf.read_csv('temp.csv')
df = cudf.read_csv('temp.csv')
print(len(df))
print(len(df.query("precip > 0")))
