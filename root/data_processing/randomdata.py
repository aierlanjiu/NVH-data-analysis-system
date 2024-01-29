import pandas as pd
import openpyxl
import random

# 读取CSV文件
df = pd.read_csv('data//Project//OriginalData//Semi Acoustic Data//data.csv', low_memory=False)

# 创建一个新的DataFrame
new_df = pd.DataFrame()

# 对偶数列进行随机增减处理
for column in df.columns:
    if column in df.columns[1::2]:
        new_col = df[column].apply(lambda x: x+random.uniform(1,30) if not isinstance(x, str) else x)

        new_df[column] = new_col
    else:
        new_col = df[column]
        new_df[column] = new_col

# 保存新的DataFrame为CSV文件
new_df.to_csv('data//Project//OriginalData//Semi Acoustic Data//updated_data.csv')
