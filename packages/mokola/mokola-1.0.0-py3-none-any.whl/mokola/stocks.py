import gse

class Stocks:

   def download(stock,start,end):
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
           return gse.downloadStock(start,end)
       else:
           return gse.downloadShareCode(stock,start,end)
        
