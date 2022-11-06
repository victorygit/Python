import pyodbc
import pandas as pd
server = 'oceanis-syn-dld-sb-ondemand.sql.azuresynapse.net'
database = 'mysql'
username = 'sqladminuser'
password = 'OPGadmin123'   

driver= '{ODBC Driver 17 for SQL Server}'

with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT TOP 3 * FROM [INFORMATION_SCHEMA].[COLUMNS]")
        row = cursor.fetchone()
        while row:
            #print (str(row[0]) + " " + str(row[1])+ " " + str(row[2])+ " " + str(row[3]))
            print(row)
            row = cursor.fetchone()
df = pd.read_sql("SELECT * FROM [INFORMATION_SCHEMA].[COLUMNS]", conn)
print(df.head(5))