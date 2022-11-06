from requests import session
from bs4 import BeautifulSoup as bs

USER = 'yzy628@gmail.com'
PASSWORD = 'victory@Git1'

URL1 = 'https://github.com/session'
URL2 = 'https://github.com/victorygit/databricks'


with session() as s:
                  
    req = s.get(URL1).text
    html = bs(req, features="lxml")
    token = html.find("input", {"name": "authenticity_token"}).attrs['value']
    com_val = html.find("input", {"name": "commit"}).attrs['value']        
    
    login_data = {'login': USER,
                  'password': PASSWORD,
                  'commit' : com_val,
                  'authenticity_token' : token}
                      
    r1 = s.post(URL1, data = login_data)
    r2 = s.get(URL2)
    print (r2)   
    soup = bs(r2.text,'html.parser')
    rows = soup.find_all('div',attrs={'class':'flex-auto min-width-0 col-md-2 mr-3','role':'rowheader'})
    for row in rows:
        link = row.find('a')['href']
        print (row.text, link)
 