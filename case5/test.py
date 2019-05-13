#!/usr/bin/env python3
import os
import pandas as pd
from datetime import datetime
import cudf
import numpy as np
from joblib import Parallel ,delayed
import sys

df = cudf.read_csv('test.csv')
df = df.sort_values(by=['RCID','Precipitation (mm)'])
#print(df.iloc[[1,2]])
