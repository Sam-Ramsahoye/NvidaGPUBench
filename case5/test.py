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
import sys

df = cudf.DataFrame([('a', list(range(20))),
('b', list(reversed(range(20)))),
('c', list(range(20)))])
print(df)