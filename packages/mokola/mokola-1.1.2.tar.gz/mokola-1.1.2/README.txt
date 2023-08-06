# Mokola
This package enables users to download stocks data from Ghana.

## Installation
```python
pip install mokola
```

## Usage

```python
import mokola.stocks.Stocks as stk
df = stk.Stocks().download('MTNGH','2021-12-01','2021-12-13')
df.head()
```

The above returns a Pandas dataframe of **MTNGH** from the stated dates *'2021-12-01'* and *'2021-12-13'* as start and end dates

You can as well all stocks data like this:
```python
import mokola.stocks.Stocks as stk
df = stk.Stocks().download(None,'2021-12-01','2021-12-13')
df.head()
```

