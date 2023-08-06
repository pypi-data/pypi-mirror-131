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