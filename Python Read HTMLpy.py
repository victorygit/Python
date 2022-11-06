import requests as rq
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_National_Football_League_career_scoring_leaders'

amount_of_pages =1  #5194 
rows = []
headers = []

for i in range(1,amount_of_pages+1):  #<-- if theres 4796 pages, your range needs to be to 4797. range goes from (start, end) but the is not inclusive of the end value
    response = rq.get(url)
    print (i)

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

df = pd.DataFrame(rows, 
               columns =headers) 
print(df.tail(20))