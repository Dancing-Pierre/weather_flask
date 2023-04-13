import numpy as np
import pandas as pd
import math
import os

df = pd.read_csv('weatherdata.csv')
df['最高温度'] = df['最高温度'].str.replace('℃','')
df['最低温度'] = df['最低温度'].str.replace('℃','')
df['风力'] = df['风力'].str.split('-').str.get(0)
df.to_csv('clean.csv')
print(df)





