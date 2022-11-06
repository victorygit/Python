import requests
from requests.auth import HTTPBasicAuth
import http.client
import json
from base64 import b64encode
import pandas as pd
import io
import xmltodict
import xml.etree.ElementTree as ET
from requests.packages.urllib3.exceptions import InsecureRequestWarning

location = 'c://temp//'
TempJsonfile = 'api.json'
Target_Json_File = location + TempJsonfile 
entity_file = location +'entity_name.csv'
df_entity = pd.read_csv(entity_file)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


for index, row in df_entity.iterrows():
    print (row['Name'])
    entity_name = row['Name']
    jr = requests.get('https://api47preview.sapsf.com/odata/v2/'+entity_name+'?', auth=('E04034@hydrooneT3', 'victory@SAP1'),verify=False)
    root = ET.fromstring(jr.content)

    Out_File_Json = open(Target_Json_File,"w+")
    Out_File_Json.write ('[\n')
    record_count = 0 
    for node in root:
        #print (node.tag)
        for child in node:
            if child.tag.find('content')> 0:
                #print(child.tag, child.attrib)                
                for childc in child:
                    if childc.tag.find('properties')> 0:
                                            
                        if record_count == 0:
                            Out_File_Json.write('{\n')
                        else:
                            Out_File_Json.write (',\n')
                            Out_File_Json.write('{\n')
                        record_count = record_count + 1
                        for childd in childc:
                            if str(childd.text) == 'None':
                                Out_File_Json.write ('"'+str(childd.tag).replace('{http://schemas.microsoft.com/ado/2007/08/dataservices}','') +'"'+':'+ '"",')
                            else:
                                Out_File_Json.write ('"'+str(childd.tag).replace('{http://schemas.microsoft.com/ado/2007/08/dataservices}','') +'"'+':'+ '"'+str(childd.text)+'",')                       
                            Out_File_Json.write ('\n')
                        Out_File_Json.write('"Dummy":"Dummmy"'+'\n')
                        Out_File_Json.write ('}')                
    Out_File_Json.write (']')
    Out_File_Json.close()
    Out_File_Json = open(Target_Json_File,"r")
    # orient='index' to avoid integer to float
    df= pd.read_json(Out_File_Json,orient='columns')
    # Remove the dummy column
    del df["Dummy"]
    # Remove the empty line
    df.drop(df.tail(1).index,
        inplace = True)
    #print (df.head(10))
    df.to_csv('c://temp//'+entity_name+'.csv', index=False)
    print (entity_name +' file is generated')
    Out_File_Json.close()
