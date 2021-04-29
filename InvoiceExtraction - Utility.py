url = "data/pdf/Oakville Hydro 20200130.pdf"

import pdfplumber
import os
import  pandas as pd 
directory = os.fsencode('C:/Documents/BI-TEK/Tax Return/2020/expence receipt/')
df= pd.DataFrame([], columns=['Filename', 'Bill Period', 'Amount'])

for subdir, dirs, files in os.walk(directory):
    for file in files:
        filename = os.fsdecode(file)
        if filename [0:14] == 'Oakville Hydro':
            url = 'C:/Documents/BI-TEK/Tax Return/2020/expence receipt/Home Untility/' + str(filename)
            print (url)
            with pdfplumber.open(url) as pdf:
                page = pdf.pages[0]
                text = page.dedupe_chars().extract_text()
            # print (text)
                for line in text.split('\n'):
                    bill_period_index = line.find('Bill Date')
                    if bill_period_index != -1 :
                         #print(line[bill_period_index:bill_period_index+9],line[bill_period_index+10:],'\n')
                        Bill_Period =  line[bill_period_index+10:]                     
                    Amount_Due_index = line.find('AMOUNT DUE')                  
                    if Amount_Due_index != -1:
                        #print(line[Amount_Due_index:Amount_Due_index+10],line[Amount_Due_index+11:],'\n')
                        df1= pd.DataFrame([[filename, Bill_Period,line[Amount_Due_index+11:Amount_Due_index+20]]], columns=['Filename', 'Bill Period', 'Amount'])
                        df = df.append(df1, ignore_index = True )
     
        if filename [0:9] == 'Union Gas':
            url = 'C:/Documents/BI-TEK/Tax Return/2020/expence receipt/Home Untility/' + str(filename)
            print (url)
            with pdfplumber.open(url) as pdf:
                for page in pdf.pages:
                    text = page.dedupe_chars().extract_text()
                    # print (text)
                    for line in text.split('\n'):
                        bill_period_index = line.find('Bill date:')
                        if bill_period_index != -1 :
                            #print(line[bill_period_index:bill_period_index+10],line[bill_period_index+11:],'\n')   
                            Bill_Period =  line[bill_period_index+11:]    
                        Amount_Due_index = line.find('Total payment now due')                  
                        if Amount_Due_index != -1:
                            #print(line[Amount_Due_index:Amount_Due_index+21],line[Amount_Due_index+22:],'\n')
                            df1= pd.DataFrame([[filename, Bill_Period,line[Amount_Due_index+22:Amount_Due_index+32]]], columns=['Filename', 'Bill Period', 'Amount'])
                            df = df.append(df1, ignore_index = True )
                        # New format after 2020 May
                        bill_period_index = line.find('Billing Period')
                        if bill_period_index != -1 :
                            #print(line[bill_period_index:bill_period_index+14],line[bill_period_index+15:],'\n') 
                            Bill_Period =  line[bill_period_index+15:]      
                        Amount_Due_index = line.find('Total Amount Due')                  
                        if Amount_Due_index != -1:
                            #print(line[Amount_Due_index:Amount_Due_index+16],line[Amount_Due_index+17:],'\n')
                            df1= pd.DataFrame([[filename, Bill_Period,line[Amount_Due_index+17:Amount_Due_index+27]]], columns=['Filename', 'Bill Period', 'Amount'])
                            df = df.append(df1, ignore_index = True )
    

df.to_csv('c:\\temp\\invoice.csv')
    