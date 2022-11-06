import logging
import azure.functions as func
import pyodbc
import pandas as pd

server = 'oceanis-syn-dld-sb-ondemand.sql.azuresynapse.net'
database = 'mysql'
driver= '{ODBC Driver 17 for SQL Server}'
authentication = 'ActiveDirectoryIntegrated'
#authentication = 'ActiveDirectoryMsi'
username = 'dbadmin'
password = 'OPGadmin123'

def main(req: func.HttpRequest) -> func.HttpResponse:
    table_name = req.params.get('table_name') 
    order_by = req.params.get('order_by')
    page_number = req.params.get('page_number')
    rows_in_page = req.params.get('rows_in_page')
    logging.info(table_name)
    #conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';Authentication='+authentication+';TrustServerCertificate=no;Encrypt=yes')
    conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    logging.info(f"DB connected")
    cursor = conn.cursor()
    sql_string = 'select * from dbo.'+ table_name + ' order by '+ order_by +' OFFSET '+ page_number +' rows fetch next '+ rows_in_page +' rows only'
    logging.info(f"sql, sql_string")
    df = pd.read_sql(sql_string,conn)
    jason_string = df.to_json(orient="table")
    logging.info(f"sql,{df.shape[0]}")

    return func.HttpResponse(
        #"This HTTP return "+str(df.shape[0])+" records"+"\n"+
        jason_string,             
        status_code=200)
    conn.close()    


