Mokola
===========
This package enables users to download stocks data from Ghana.

Installation
-------------
```bash
pip install mokola
```

Usage
=============
Download Specific Stock Data
-----------------------------
```python
import mokola.stocks.Stocks as stk
df = stk.Stocks().download('MTNGH','2021-12-01','2021-12-13')
df.head()
```