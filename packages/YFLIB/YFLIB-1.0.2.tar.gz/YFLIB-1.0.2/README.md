# Python_YFLib
- Providing both dayEnd and indicator function
- Using YFinance as source
- All called function would save a cache in local
- *** SUDO *** root permission required

---
## How to import?
- ``` from yflib import functions ```
---
## Library Included

1. Yfinance
2. Pandas
3. Numpy
---
## Day End

### Read data of day end

- Start date and End date are inclusive
```
    functions.read_dayEnd(stock,startDate,endDate,useCols,verbose)
```
| Params      | Type        | Example        | Optional |
| ----------- | ----------- | -------------- | -------- | 
| stock       | string      | "AAPL"         | F        |
| starDate    | string      | "2000-01-05"   | T        |
| endDate     | string      | "2000-01-09"   | T        |
| useCols     | List        | ["Open","Low"] | T        |
| verbose     | Boolean     | True           | T        |

- useCols full list
```
    [open, high, low, close, adjusted_close, volume, dividend_amount, split_coefficient]
```

---
## Indicators
- Series type: close
  
### Read data of day end
- Start date and End date are inclusive
```
    functions.read_indicator(stock,indicator,startDate,endDate,useCols,verbose)
```
| Params      | Type        | Example        | Optional |
| ----------- | ----------- | -------------- | -------- | 
| stock       | string      | "AAPL"         | F        |
| indicator   | string      | "SMA"          | F        |
| period      | Number      | 12             | T        |
| starDate    | string      | "2000-01-05"   | T        |
| endDate     | string      | "2000-01-09"   | T        |
| verbose     | Boolean     | True           | T        |


### 1. SMA
- Period: 50/200

### 2. EMA
- Period: 50/200

### 3. MACD
<!-- - Period: 9/12/26 -->

### 4. STOCH
- Period: NULL

### 5. RSI
- Period: 9/14

### 6. STOCHRSI
- Period: 60/120

### 7. CCI
- Period: 14/50

### 8. BBRANDS
- Period: Null (Default 20 fixed)

### 9. OBV
- Period: Null

---

` version = 1.0.2 `