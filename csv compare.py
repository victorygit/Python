import pandas as pd
import datacompy
df0 =pd.read_csv('C:/Users/yzy62/Downloads/SQL_script_0.csv')
df1 =pd.read_csv('C:/Users/yzy62/Downloads/SQL_script_1.csv')
df0_column = df0.columns
df0_size = df0.size
df1_column = df1.columns
df1_size = df0.size
print('Source size is:',df0_size)
print('Target szie is:',df1_size)
print(df0.equals(df1))
print(df0.head(10))
compare = datacompy.Compare(
df0,
df1,
join_columns='BUKRS',
abs_tol=0.0001,
rel_tol=0,
df1_name='original',
df2_name='new')
print(compare.report())