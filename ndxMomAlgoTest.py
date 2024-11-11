# This file tests the Momentum stragegy
import pandas as pd
import pandas_market_calendars as mcal
import datetime
nyse = mcal.get_calendar('NYSE')
a = nyse.valid_days(start_date='2024-01-01', end_date='2024-11-08')
print(a)

NumberOfStocks = 5

from FuncProgTrade import getSortedIndexReturns
from FuncProgTrade import getReturnsOfLongShortPortfolio

print(datetime.datetime.strftime(a[0],'%Y-%m-%d'))
TotalReturnList = list()
DateReturnList = list()
for i in range(1,len(a)):

#for i in range(1,2):
    LongStockList = list()
    ShortStockList = list()
    # Prior day input for the trading algo
    RunDate = datetime.datetime.strftime(a[i-1],'%Y-%m-%d')
    print("Prior date = ", RunDate)
    dfPctChange = getSortedIndexReturns(RunDate)
    print("dfPctChange")
    print(dfPctChange)

    # Now that we have the sorted Returns, lets trade the top and bottom performers.
    # The idea is to play momentum. Lets go long the top x names and short the bottom x names
    # Idea is that we put the trade on at the beginning of the day...so we get Open price and close out at
    # the end of day at the Close price.
    for j in range(0,len(dfPctChange)):
        LongStockList.append(dfPctChange.loc[j,'Ticker'])
        if len(LongStockList)>=NumberOfStocks:
            break
    for j in range(len(dfPctChange)-1,0,-1):
        ShortStockList.append(dfPctChange.loc[j,'Ticker'])
        if len(ShortStockList)>=NumberOfStocks:
            break
    print("Long Stocks: ", LongStockList)
    print("Short Stocks: ", ShortStockList)

    # Lets get the return of this Long/short portfolio over the day
    RunDate = datetime.datetime.strftime(a[i], '%Y-%m-%d')
    print("Test date = ", RunDate)
    ReturnDict = getReturnsOfLongShortPortfolio(RunDate,LongStockList,ShortStockList)

    TotalReturn = (sum(ReturnDict['Long']) + sum(ReturnDict['Short']))/NumberOfStocks

    print("Return Dict: ", ReturnDict)
    print("Total Return: ", TotalReturn)
    TotalReturnList.append(TotalReturn)
    DateReturnList.append(RunDate)


DictOut = {'Date':DateReturnList,'Return':TotalReturnList}

dfOut = pd.DataFrame(DictOut)

dfOut.to_csv("ReturnData.csv")





