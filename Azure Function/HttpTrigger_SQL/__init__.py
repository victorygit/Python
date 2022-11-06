import logging
import azure.functions as func
import pyodbc
import pandas as pd

password = 'OPGadmin123'
server = 'ds-dataload-sql-sb.database.windows.net'
database = 'dataload-sqldb'
username = 'dbadmin'
driver= '{ODBC Driver 17 for SQL Server}'


def main(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('name')
    conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()
    df = pd.read_sql('select * from [dbo].[Batch_Register]',conn)
    jason_string = df.to_json(orient="table")
    logging.info(f"sql,{df.shape[0]}")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function return {df.shape[0]} records.")
    else:
        return func.HttpResponse(
             #"This HTTP return "+str(df.shape[0])+" records"+"\n"+
             jason_string,             
             status_code=200)
    conn.close()    


