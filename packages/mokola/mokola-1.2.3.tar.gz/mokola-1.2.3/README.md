Mokola
===========
This package enables users to download stocks data from Ghana.

Installation
-------------
```
pip install mokola
```

Usage
=============
Download Specific Stock Data
-----------------------------
```
import mokola.stocks.Stocks as stk
```

```
df = stk.Stocks().download('MTNGH','2021-12-01','2021-12-13')
```

Download All Data for a period
------------------------------
You can as well all stocks data like this

```
import mokola.stocks.Stocks as stk
```

```
df = stk.Stocks().download(None,'2021-12-01','2021-12-13')
```