import os
import pandas as pd
import datetime
from datetime import datetime
import math
import numpy as np

def gettime(row): 
    vtime = row['datetime'][11:16]
    if len(vtime) < 5:
        vtime = "0"+vtime    
    return vtime
def gethour(row):  
    return row['oritime'][0:2]
def getmins(row):  
    return row['oritime'][3:5]
def getnewTime(row):
    if int(row['Mins']) < 15:
        vmins = '00'
    else:
        if int(row['Mins']) < 30:
            vmins = '15'
        else:
            if int(row['Mins']) < 45:
                vmins = '30'
            else:
                vmins = '45'             
    vnewtime = row['Hour']+":"+vmins
    return vnewtime
def cleanwaittime(row):
    if row['SPOSTMIN'] == -999:
        vwaittime = np.nan
    else:
        #if (row['SPOSTMIN'] == 0 or math.isnan(row['SPOSTMIN'])) and (row['SACTMIN'] != 0):
        #    vwaittime = row['SACTMIN']
        #else:
        vwaittime = row['SPOSTMIN']
    return vwaittime

df_whole = pd.DataFrame()
directory = os.path.join("G:\\","My Drive\\Cindy\\IB11\\Math IA\\ridedata")
for root,dirs,files in os.walk(directory):
    for file in files:
       if file.endswith(".csv"):
        print(file)
        df = pd.read_csv("G:\\My Drive\\Cindy\\IB11\\Math IA\\ridedata\\"+file, header=0)
        df_whole = df_whole.append(df)
df_whole.info()
df_whole['oritime'] = df_whole.apply(lambda row: gettime(row), axis=1)
df_whole['Hour'] = df_whole.apply(lambda row: gethour(row), axis=1)
df_whole['Mins'] = df_whole.apply(lambda row: getmins(row), axis=1)
df_whole['NewTime'] = df_whole.apply(lambda row: getnewTime(row), axis=1)
df_whole['Waittime']  = df_whole.apply(lambda row: cleanwaittime(row), axis=1)
df_whole['Waittime'] = df_whole['Waittime'].fillna(method='ffill')
#print(df_whole[df_whole.SPOSTMIN == -999])
df_whole.to_csv("G:\\My Drive\\Cindy\\IB11\\Math IA\\ridedatanew\\rides.csv", header=True)
print("---------------- Done ----------------------")