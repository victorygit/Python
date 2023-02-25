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

server = 'oceanis-syn-finance-dev-ondemand.sql.azuresynapse.net'
database = 'synwssqlpool'
username ='victor.yang@opg.com'
Authentication='ActiveDirectoryInteractive'
driverad= '{ODBC Driver 17 for SQL Server}'
connad = pyodbc.connect('DRIVER='+driver+
                      ';SERVER='+server+
                      ';PORT=1433;DATABASE='+database+
                      ';UID='+username+
                      ';AUTHENTICATION='+Authentication
                      )

print(connad)
with connad.cursor() as cursorad:
    cursorad.execute("SELECT TOP 3 * FROM [INFORMATION_SCHEMA].[COLUMNS]")
    rowad = cursorad.fetchone()
    while rowad:
    #print (str(row[0]) + " " + str(row[1])+ " " + str(row[2])+ " " + str(row[3]))
        print(rowad)
        rowad = cursorad.fetchone()
df_ad = pd.read_sql("SELECT * FROM [INFORMATION_SCHEMA].[COLUMNS]", connad)
print(df_ad.head(5))