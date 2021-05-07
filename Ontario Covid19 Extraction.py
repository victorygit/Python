#import urllib.request
#with urllib.request.urlopen("https://data.ontario.ca/api/3/action/datastore_search?resource_id=455fd63b-603d-4608-8216-7d8647f43350") as url:
#    s = url.read()
#    # I'm guessing this would output the html source code ?
#    print(s)


import pandas as pd

mytable = pd.read_table("https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv",sep=",")
print(mytable.head(10))
mytable.to_csv("C:\Documents\Victor\Covid\conposcovidloc.csv")