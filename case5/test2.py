import cudf
df = cudf.DataFrame([('a', list(range(20))),
('b', list(reversed(range(20)))),
('c', list(range(20)))])
print(df.iloc[[1,2]])
