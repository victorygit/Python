import requests
import pandas as pd
# url for API
url = 'http://dataserviceapio-ibzr.us-e2.cloudhub.io/data?format=json'
req = requests.get(url)

#print(req.status_code)
#print(req.headers)
#print(req.text)

df=pd.read_json(req.text)
print(df.head(10))

url = 'http://dataserviceapio-ibzr.us-e2.cloudhub.io/data?format=csv'
req = requests.get(url)
print(req.status_code)
print(req.headers)
print(req.text)
df = pd.read_csv(req.text )
print(df.head(2))