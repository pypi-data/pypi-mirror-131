import pandas as pd
import urllib
import requests

def downloadStock(start,end):
    headers = {'Content-Type': 'application/json'}
    response = requests.get('https://logiclabent.com/mokola/v1/stocks/'+start+'/'+end+'/period',headers=headers)
    results =response.json()
    return pd.DataFrame(results)

def downloadShareCode(sharecodes,start,end):
    headers = {'Content-Type': 'application/json'}
    response = requests.get('https://logiclabent.com/mokola/v1/stocks/'+sharecodes+"/"+start+"/"+end+"/dated",headers=headers)
    results =response.json()
    return pd.DataFrame(results)