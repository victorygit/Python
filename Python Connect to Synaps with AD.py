import logging
import azure.functions as func
import pyodbc
import pandas as pd
user = 'victor.yang@opg.com'
server = 'oceanis-syn-dld-sb-ondemand.sql.azuresynapse.net'
database = 'mysql'
driver= '{ODBC Driver 17 for SQL Server}'
authentication = 'ActiveDirectoryIntegrated'
#authentication = 'ActiveDirectoryMsi'
username = 'dbadmin'
password = 'OPGadmin123'
#conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';Authentication='+authentication+';TrustServerCertificate=no;Encrypt=yes')
conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = conn.cursor()
df = pd.read_sql('select * from dbo.Nakisa_Orgunit_External',conn)
jason_string = df.to_json(orient="table")
conn.close()    
