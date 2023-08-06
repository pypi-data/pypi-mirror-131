import pandas as pd
import urllib
import requests

class Stocks:
   def downloadStock(self,start,end):
    headers = {'Content-Type': 'application/json'}
    response = requests.get('https://logiclabent.com/mokola/v1/stocks/'+start+'/'+end+'/period',headers=headers)
    results =response.json()
    return pd.DataFrame(results)

   def downloadShareCode(self,sharecodes,start,end):
      headers = {'Content-Type': 'application/json'}
      response = requests.get('https://logiclabent.com/mokola/v1/stocks/'+sharecodes+"/"+start+"/"+end+"/dated",headers=headers)
      results =response.json()
      return pd.DataFrame(results)

   def download(self,stock,start,end):
       """Download stock market data by passing the stock code or the start and end date you need.
    
        Parameters
        ----------
        stock : str
            The share code of the company being looked for
        start : str
            The start date of the data. It can be in the form yyyy-MM-dd
        end : str   
           The end date of the data. It should be in the form yyyy-MM-dd   
    
       Returns
       --------
          DataFrame
               a dataframe of the relevant stock data based on the supplied parameters
       """
       if stock==None:
           return self.downloadStock(start,end)
       else:
           return self.downloadShareCode(stock,start,end)
        
