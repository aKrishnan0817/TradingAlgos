import yfinance as yf
import pandas as pd
import datetime

def getSortedIndexReturns(RunDate):
    #RunDate = '2024-11-08'

    PctChangeList = list()
    TickerList = list()
    df = pd.read_csv("Nasdaq100MembersJan2024.csv",header = None)
    df.columns = ['members']

    for i in range(0,len(df)):
        aa = df.loc[i,'members']
        b = aa.find(" ")

        ticker = aa[:b]
        print("ticker: ", ticker)
        # Lets loop through all the NASDAQ members and see which one has either positive or negative momentum

        # Lets find price change over a specified period of time.
        TimeInput = 5 # 5 days prior
        RunDateObj = datetime.datetime.strptime(RunDate,'%Y-%m-%d')
        d = datetime.timedelta(days = TimeInput)
        a = RunDateObj-d
        StartDateStr = datetime.datetime.strftime(a,'%Y-%m-%d')

        print(StartDateStr)

        data = yf.download(ticker, start=StartDateStr, end=RunDate,multi_level_index=False)
        data = data.reset_index()
        print(data)
        print(data['Close'].values)
        print(data['Date'])
        a1 = data.loc[0,'Date']
        print(datetime.datetime.strftime(a1,'%Y-%m-%d'))
        PriceData = data['Close'].values
        print("PriceData : ", PriceData)
        print(PriceData[-1])
        PctChange = (PriceData[-1]-PriceData[0])/PriceData[0]
        print(PctChange)
        PctChangeList.append(PctChange)
        TickerList.append(ticker)

    mydict = {'Ticker': TickerList,'PctChange':PctChangeList}

    dfChange = pd.DataFrame(mydict)
    dfChange = dfChange.sort_values('PctChange',ascending=False)
    dfChange =dfChange.reset_index()
    print(dfChange)

    return dfChange

def getReturnsOfLongShortPortfolio(RunDate,LongStockList, ShortStockList):
    LongReturnList = list()
    ShortReturnList = list()
    for i in range(0,len(LongStockList)):
        ticker = LongStockList[i]
        RunDateObj = datetime.datetime.strptime(RunDate, '%Y-%m-%d')
        d = datetime.timedelta(days=4)
        a = RunDateObj - d
        StartDateStr = datetime.datetime.strftime(a, '%Y-%m-%d')


        data = yf.download(ticker, start=StartDateStr, end=RunDate, multi_level_index=False)
        data = data.reset_index()
        OpenPrice = data['Open'].values
        ClosePrice = data['Close'].values

        print("OpenPrice: ",OpenPrice)
        print("ClosePrice: ",ClosePrice)
        Return = (ClosePrice[-1]-OpenPrice[-1])/OpenPrice[-1]
        LongReturnList.append(Return)

    for i in range(0,len(ShortStockList)):
        ticker = ShortStockList[i]
        RunDateObj = datetime.datetime.strptime(RunDate, '%Y-%m-%d')
        d = datetime.timedelta(days=4)
        a = RunDateObj - d
        StartDateStr = datetime.datetime.strftime(a, '%Y-%m-%d')


        data = yf.download(ticker, start=StartDateStr, end=RunDate, multi_level_index=False)
        data = data.reset_index()
        OpenPrice = data['Open'].values
        ClosePrice = data['Close'].values

        print("OpenPrice: ",OpenPrice)
        print("ClosePrice: ",ClosePrice)
        Return = -(ClosePrice[-1]-OpenPrice[-1])/OpenPrice[-1]
        ShortReturnList.append(Return)

    RetDict = {'Long':LongReturnList,'Short':ShortReturnList}

    return RetDict


