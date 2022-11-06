import pandas as pd


df = pd.read_json("D:\Documents\BI-TEK\OPG\Ariba\Ariba_Analytics_Document_Type.json")
df.to_csv("D:\Documents\BI-TEK\OPG\Ariba\Ariba_Analytics_Document_Type.csv")