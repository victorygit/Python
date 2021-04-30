

import pdfplumber
import os
    

url = 'C:/Documents/BI-TEK/Tax Return/2020/expence receipt/Cell Phone/Fido-Feb13_2020.pdf' 
#url = 'C:/Documents/BI-TEK/Tax Return/2020/expence receipt/Online Order/Staple 2020-05-23.pdf'
stop = False
start = False
with pdfplumber.open(url) as pdf:
    for page in pdf.pages:
        text = page.dedupe_chars().extract_text()
        print(text)
        for line in text.split('\n'):
            bill_period_index = line.find('2137501055')
            if bill_period_index != -1 :
                #print(line[bill_period_index:bill_period_index+10],line[bill_period_index+11:35],'\n')   
                Bill_Period =  line[bill_period_index+11:35] 
                if  line.find('Mobile 647-886-0251') != -1:
                    start = True
                    if start == True:
                        Tax_index = line.find('HST: 815781448')                  
                        if Tax_index != -1:
                            Tax_amount = line[Tax_index+15:25]  
                        Amount_Due_index = line.find('Total for Mobile 647-621-2806')                  
                        if Amount_Due_index != -1:
                            #print(line[Amount_Due_index:Amount_Due_index+30],line[Amount_Due_index+31:],'\n')    
                            stop = True
                            break
        if stop == True:
            break