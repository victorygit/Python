
import pdfplumber
import os
import  pandas as pd 
directory = os.fsencode('C:/Documents/BI-TEK/Tax Return/2020/expence receipt/Cell Phone')
df= pd.DataFrame([], columns=['Filename', 'Bill Period', 'Amount'])

for file in os.listdir(directory):
     filename = os.fsdecode(file)
     stop = False
     if filename [0:5] == 'Fido-':
        url = 'C:/Documents/BI-TEK/Tax Return/2020/expence receipt/Cell Phone/' + str(filename)
        print (url)
        with pdfplumber.open(url) as pdf:
            for page in pdf.pages:
                text = page.dedupe_chars().extract_text()
                for line in text.split('\n'):
                    bill_period_index = line.find('2137501055')
                    if bill_period_index != -1 :
                        print(line[bill_period_index:bill_period_index+10],line[bill_period_index+11:35],'\n')   
                        Bill_Period =  line[bill_period_index+11:35] 
                    Amount_Due_index = line.find('Total for Mobile 647-621-2806')                  
                    if Amount_Due_index != -1:
                        print(line[Amount_Due_index:Amount_Due_index+30],line[Amount_Due_index+31:],'\n')    
                        df1= pd.DataFrame([[filename, Bill_Period,line[Amount_Due_index+22:Amount_Due_index+32]]], columns=['Filename', 'Bill Period', 'Amount'])
                        df = df.append(df1, ignore_index = True )
                        stop = True
                        break
                if stop == True:
                    break
     
     if filename [0:9] == 'Union Gas':
        url = 'C:/Documents/BI-TEK/Tax Return/2020/expence receipt/Cell Phone/' + str(filename)
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
    