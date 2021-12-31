

import pdfplumber
import os
    

url = 'D:/Documents/BI-TEK/Tax Return/2021/expence receipt/Phone & Internet/ItalkBB BillingDetail_202101.pdf' 
#url = 'C:/Users/yzy62/Downloads/BellPDF_Print.pdf'
stop = False
start = False
Tax_amount = 0
with pdfplumber.open(url) as pdf:
    for page in pdf.pages:
        text = page.dedupe_chars().extract_text()
        print(text)
        for line in text.split('\n'):
                        bill_period_index = line.find('How to Contact Us: Billing Date:')
                        if bill_period_index != -1 :                            
                            #print(line[bill_period_index:bill_period_index+11],line[bill_period_index+12:],'\n')   
                            Bill_Period =  line[bill_period_index+33:] 
                        Tax_index = line.find('  HST:838692754 RT0001')                  
                        if Tax_index != -1:
                            Tax_amount = line[Tax_index+25:]     
                        Amount_Due_index = line.find('Total:')                  
                        if Amount_Due_index != -1:                            
                            Amount_due = line[Amount_Due_index+9:]                            
                            #df1= pd.DataFrame([[filename, Bill_Period,line[Amount_Due_index+21:Amount_Due_index+41],Tax_amount]], columns=['Filename', 'Bill Period', 'Amount','Tax'])
                            #df = df.append(df1, ignore_index = True )

print("\n Result\n")
print (Bill_Period)
print (Amount_due)
print(Tax_amount )