
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import *
from functools import *
from pyspark import SparkContext, SparkConf, SQLContext
import pyodbc
import pandas as pd
from pyspark.sql import SparkSession

driver= '{ODBC Driver 17 for SQL Server}'
server = "oceanis-syn-dev-ondemand.sql.azuresynapse.net"  # 'tcp:myserver.database.windows.net', 'localhost\sqlexpress'
database = "synwssqlpool"
username = "API_Reader"
password = "OPGapi1234"
conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
df1 = pd.read_sql("SELECT * FROM SAPBWFRA.vwMST_JOB", conn)
df2 = pd.read_sql("SELECT * FROM SAPBWFRA.vwMST_JOB", conn)
df_comp = df1.compare(df2)
print(df_comp.count())
spark = SparkSession.builder \
    .master("local[1]") \
    .appName("SparkByExamples.com") \
    .getOrCreate()
#Create PySpark DataFrame from Pandas
sparkDF1=spark.createDataFrame(df1) 
sparkDF2=spark.createDataFrame(df2) 
sparkDF2.show()
sparkdf_comp = sparkDF1.subtract(sparkDF2)
print(sparkdf_comp.count())