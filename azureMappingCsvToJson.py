import pandas as pd
import json

df =pd.read_csv('D:\Documents\Python\Input\csvtoJson.csv', header=0)
#print(df)
dictionary_translator ={}
dictionary_mapping ={}
mapping = []
dfa = df[df.file == 'A']
print(dfa)
for index,row in dfa.iterrows():
    print(row)
    dictionary_map = {}
    dictionary_sourcefield = {}
    dictionary_sinkfield = {}
    dictionary_sourcefield['name'] =row.field
    dictionary_sourcefield['type'] =row.type
    dictionary_sinkfield['name'] =row.field
    dictionary_sinkfield['type'] =row.type
    dictionary_map['source'] = dictionary_sourcefield
    dictionary_map['sink'] = dictionary_sinkfield
    mapping.append(dictionary_map)
dictionary_mapping['type']= 'TabularTranslator'
dictionary_mapping['mappings'] = mapping
dictionary_translator['translator'] = dictionary_mapping
json_string = json.dumps(dictionary_translator)
print (json_string)
