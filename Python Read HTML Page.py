import requests as rq
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_National_Football_League_career_scoring_leaders'

rows = []
headers = []

response = rq.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text,'html.parser')
    #print(soup)
    table = soup.find('table',attrs={'class':'wikitable sortable'})
    #print(table)
    if len(headers) == 0:
        for th in table.find("tr").find_all("th"):
            headers.append(th.text.strip())
        headers.append('URL')

    for tr in table.find_all("tr")[1:]:
        cells = []
        tds = tr.find_all("td")
        for td in tds:
            cells.append(td.text.strip())
            if td.find('a'):
                link = td.find('a')['href']
                #print(link)
        cells = cells + [link]        
        rows.append(cells)

df = pd.DataFrame(rows, columns =headers) 
print(df.tail(20))