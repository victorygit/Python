url = "data/pdf/Oakville Hydro 20200130.pdf"

import pdfplumber
import os
import  pandas as pd 
dir_str= 'D:/Documents/BI-TEK/Tax Return/2022/expence receipt/'
directory = os.fsencode(dir_str)
df= pd.DataFrame([], columns=['Filename', 'Bill Period', 'Amount', 'Tax'])
Tax_amount = 0

for subdir, dirs, files in os.walk(directory):    
    for file in files:
        filename = os.fsdecode(file)
        if filename [0:14] == 'Oakville Hydro':
            url = dir_str+'Home Untility/' + str(filename)
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
                    Tax_index = line.find('H.S.T. # 869177972')                  
                    if Tax_index != -1:
                        Tax_amount = line[Tax_index+19:]                       
                    Amount_Due_index = line.find('AMOUNT DUE')                  
                    if Amount_Due_index != -1:
                        #print(line[Amount_Due_index:Amount_Due_index+10],line[Amount_Due_index+11:],'\n')
                        df1= pd.DataFrame([[filename, Bill_Period,line[Amount_Due_index+11:Amount_Due_index+20],Tax_amount]], columns=['Filename', 'Bill Period', 'Amount', 'Tax'])
                        df = df.append(df1, ignore_index = True )
     
        if filename [0:9] == 'Union Gas':
            url = dir_str +'Home Untility/' + str(filename)
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
                        Tax_index = line.find('HST')                  
                        if Tax_index != -1:
                            Tax_amount = line[Tax_index+4:14]                            
                        Amount_Due_index = line.find('Total payment now due')                  
                        if Amount_Due_index != -1:
                            #print(line[Amount_Due_index:Amount_Due_index+21],line[Amount_Due_index+22:],'\n')
                            df1= pd.DataFrame([[filename, Bill_Period,line[Amount_Due_index+22:Amount_Due_index+32],Tax_amount]], columns=['Filename', 'Bill Period', 'Amount', 'Tax'])
                            df = df.append(df1, ignore_index = True )
                        # New format after 2020 May
                        bill_period_index = line.find('Billing Period')
                        if bill_period_index != -1 :
                            #print(line[bill_period_index:bill_period_index+14],line[bill_period_index+15:],'\n') 
                            Bill_Period =  line[bill_period_index+15:]      
                        Amount_Due_index = line.find('Total Charges for Natural Gas')                  
                        if Amount_Due_index != -1:
                            #print(line[Amount_Due_index:Amount_Due_index+16],line[Amount_Due_index+30:],'\n')
                            df1= pd.DataFrame([[filename, Bill_Period,line[Amount_Due_index+30:Amount_Due_index+47],Tax_amount]], columns=['Filename', 'Bill Period', 'Amount', 'Tax'])
                            df = df.append(df1, ignore_index = True )

        if filename [0:12] == 'Enbridge Gas':
            url = dir_str +'Home Untility/' + str(filename)
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
                        Tax_index = line.find('HST')                  
                        if Tax_index != -1:
                            Tax_amount = line[Tax_index+4:14]                            
                        Amount_Due_index = line.find('Total payment now due')                  
                        if Amount_Due_index != -1:
                            #print(line[Amount_Due_index:Amount_Due_index+21],line[Amount_Due_index+22:],'\n')
                            df1= pd.DataFrame([[filename, Bill_Period,line[Amount_Due_index+22:Amount_Due_index+32],Tax_amount]], columns=['Filename', 'Bill Period', 'Amount', 'Tax'])
                            df = df.append(df1, ignore_index = True )
                        # New format after 2020 May
                        bill_period_index = line.find('Billing Period')
                        if bill_period_index != -1 :
                            #print(line[bill_period_index:bill_period_index+14],line[bill_period_index+15:],'\n') 
                            Bill_Period =  line[bill_period_index+15:]      
                        Amount_Due_index = line.find('Total Charges for Natural Gas')                  
                        if Amount_Due_index != -1:
                            #print(line[Amount_Due_index:Amount_Due_index+16],line[Amount_Due_index+30:],'\n')
                            df1= pd.DataFrame([[filename, Bill_Period,line[Amount_Due_index+30:Amount_Due_index+47],Tax_amount]], columns=['Filename', 'Bill Period', 'Amount', 'Tax'])
                            df = df.append(df1, ignore_index = True )
    
        if filename [0:6] == 'Cogeco':
            url = dir_str +'Phone & Internet/' + str(filename)
            print (url)
            stop = False
            with pdfplumber.open(url) as pdf:
                for page in pdf.pages:
                    text = page.dedupe_chars().extract_text()
                    # print (text)
                    for line in text.split('\n'):
                        bill_period_index = line.find('BillingDate')
                        if bill_period_index != -1 :
                            #print(line[bill_period_index:bill_period_index+11],line[bill_period_index+12:],'\n')   
                            Bill_Period =  line[bill_period_index+12:] 
                        Tax_index = line.find('HST')                  
                        if Tax_index != -1:
                            Tax_amount = line[Tax_index+4:13]     
                        Amount_Due_index = line.find('Currentmonthsubtotal')                  
                        if Amount_Due_index != -1:
                            #print(line[Amount_Due_index:Amount_Due_index+20],line[Amount_Due_index+21:],'\n')
                            df1= pd.DataFrame([[filename, Bill_Period,line[Amount_Due_index+21:Amount_Due_index+41],Tax_amount]], columns=['Filename', 'Bill Period', 'Amount','Tax'])
                            df = df.append(df1, ignore_index = True )
                            stop = True
                            break
                    if stop == True:
                        break

        if filename [0:5] == 'Fido-':
            url = dir_str +'Cell Phone/' + str(filename)
            print (url)
            stop = False
            start = False
            with pdfplumber.open(url) as pdf:
                for page in pdf.pages:
                    text = page.dedupe_chars().extract_text()
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
                                Tax_amount = line[Tax_index+15:20]  
                            Amount_Due_index = line.find('Total for Mobile 647-886-0251')                  
                            if Amount_Due_index != -1:
                                #print(line[Amount_Due_index:Amount_Due_index+30],line[Amount_Due_index+31:],'\n')    
                                df1= pd.DataFrame([[filename, Bill_Period,line[Amount_Due_index+30:Amount_Due_index+35],Tax_amount]], columns=['Filename', 'Bill Period', 'Amount','Tax'])
                                df = df.append(df1, ignore_index = True )
                                stop = True
                                break
                    if stop == True:
                        break
        if filename [0:7] == 'BellPDF':
            url = dir_str +'Cell Phone/' + str(filename)
            print (url)
            stop = False
            start = False
            with pdfplumber.open(url) as pdf:
                text = pdf.pages[0].dedupe_chars().extract_text()
                for page in pdf.pages:
                    text = page.dedupe_chars().extract_text()
                    for line in text.split('\n'):
                        if  line.find('Mobile Number 647-886-0251') != -1:
                            start = True
                        if start == True:
                            bill_period_index = line.find('Monthly charges billed to')
                            if bill_period_index != -1 :
                                #print(line[bill_period_index:bill_period_index+25],line[bill_period_index+26:37],'\n')   
                                Bill_Period =  line[bill_period_index+26:37] 
                            Tax_index = line.find('HST')                  
                            if Tax_index != -1:
                                Tax_amount = line[Tax_index+3:13]  
                            Amount_Due_index = line.find('Total current charges')                  
                            if Amount_Due_index != -1:
                                #print(line[Amount_Due_index:Amount_Due_index+21],line[Amount_Due_index+22:],'\n')    
                                df1= pd.DataFrame([[filename, Bill_Period,line[Amount_Due_index+22:Amount_Due_index+32],Tax_amount]], columns=['Filename', 'Bill Period', 'Amount','Tax'])
                                df = df.append(df1, ignore_index = True )
                                stop = True
                                break
                    if stop == True:
                        break
        if filename [0:13] == 'Bell Internet':
            url = dir_str +'Phone & Internet/' + str(filename)
            print (url)
            stop = False
            with pdfplumber.open(url) as pdf:
                for page in pdf.pages:
                    text = page.dedupe_chars().extract_text()
                    # print (text)
                    for line in text.split('\n'):
                        bill_period_index = line.find('267486146')
                        if bill_period_index != -1 :
                            #print(line[bill_period_index:bill_period_index+9],line[bill_period_index+10:39],'\n')
                            Bill_Period =  line[bill_period_index+10:39]  
                        Tax_index = line.find('Taxes')                  
                        if Tax_index != -1:
                            Tax_amount = line[Tax_index+5:]       
                        Amount_Due_index = line.find('Amount due')                  
                        if Amount_Due_index != -1:
                            #print(line[Amount_Due_index:Amount_Due_index+10],line[Amount_Due_index+11:20],'\n')                   
                            df1= pd.DataFrame([[filename, Bill_Period,line[Amount_Due_index+11:Amount_Due_index+20],Tax_amount]], columns=['Filename', 'Bill Period', 'Amount','Tax'])
                            df = df.append(df1, ignore_index = True )
                            stop = True
                            break
                    if stop == True:
                        break
        if filename [0:6] == 'Staple':
            url =dir_str +'Online Order/' + str(filename)
            print (url)
            find_tax  = False
            stop = False
            with pdfplumber.open(url) as pdf:
                for page in pdf.pages:
                    text = page.dedupe_chars().extract_text()
                    for line in text.split('\n'):
                    #bill_period_index = line.find('DATE')
                    #if bill_period_index != -1 :
                    #print(line[bill_period_index:bill_period_index+4],line[bill_period_index+5],'\n')  
                        Tax_index = line.find('HST 13%')                  
                        if Tax_index != -1:
                            #print(line[Tax_index:+Tax_index+7],line[Tax_index+8:],'\n')     
                            Tax_amount = line[Tax_index+8:18]
                            find_tax = True
                        if find_tax == True:
                            Amount_Due_index = line.find('Total')                  
                            if Amount_Due_index != -1:
                                #print(line[Amount_Due_index:Amount_Due_index+5],line[Amount_Due_index+6:],'\n')
                                df1= pd.DataFrame([[filename, '', line[Amount_Due_index+5:Amount_Due_index+15],Tax_amount]], columns=['Filename', 'Bill Period', 'Amount','Tax'])
                                df = df.append(df1, ignore_index = True )
                                stop = True
                                break
                    if stop == True:
                        break        
        if filename [0:14] == 'Amazon invoice':
            url =dir_str +'Online Order/' + str(filename)
            print (url)
            Amount_Due = 0
            Tax_Amount = 0
            with pdfplumber.open(url) as pdf:
                for page in pdf.pages:
                    text = page.dedupe_chars().extract_text()
                    for line in text.split('\n'):
                        bill_period_index = line.find('Invoice date / Date de facturation:')
                        if bill_period_index != -1 :                            
                            #print(line[bill_period_index:bill_period_index+11],line[bill_period_index+12:],'\n')   
                            Invoice =  line[bill_period_index+36:]  
                        Amount_Due_index = line.find('Total $')                  
                        if Amount_Due_index != -1:                            
                            Amount = line[Amount_Due_index+6:]
                            amount_list = Amount.replace('$','').split(' ')  
                            tax_col_number = len(amount_list)-1
                            #print(amount_list)                   
                            Amount_Due = Amount_Due +  float(amount_list[0])+float(amount_list[tax_col_number])
                            Tax_Amount = Tax_Amount  +float(amount_list[tax_col_number])
                df1= pd.DataFrame([[filename, Invoice,Amount_Due,Tax_Amount]], columns=['Filename', 'Bill Period', 'Amount','Tax'])
                df = df.append(df1, ignore_index = True )
        if filename [0:21] == 'ItalkBB BillingDetail':
            url =dir_str +'Phone & Internet/' + str(filename)
            print (url)
            Amount_Due = 0
            Tax_Amount = 0
            with pdfplumber.open(url) as pdf:
                for page in pdf.pages:
                    text = page.dedupe_chars().extract_text()
                    for line in text.split('\n'):
                        bill_period_index = line.find('How to Contact Us: Billing Date:')
                        if bill_period_index != -1 :                            
                            #print(line[bill_period_index:bill_period_index+11],line[bill_period_index+12:],'\n')   
                            Bill_Period =  line[bill_period_index+33:] 
                        Tax_index = line.find('  HST:838692754 RT0001')                  
                        if Tax_index != -1:
                            Tax_Amount = line[Tax_index+25:]     
                        Amount_Due_index = line.find('Total:')                  
                        if Amount_Due_index != -1:                            
                            Amount_Due = line[Amount_Due_index+9:]                                              
                df1= pd.DataFrame([[filename, Invoice,Amount_Due,Tax_Amount]], columns=['Filename', 'Bill Period', 'Amount','Tax'])
                df = df.append(df1, ignore_index = True )
                    
print(df.head(10))
df.to_csv('d:/temp/invoice.csv')
    