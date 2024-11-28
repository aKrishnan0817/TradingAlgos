#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pandas_market_calendars as mcal
import datetime
import yfinance as yf
import pickle
import os


# In[ ]:
def get_calendar():
    nyse = mcal.get_calendar('NYSE')
    a = nyse.valid_days(start_date='2014-01-01', end_date='2024-11-14')
    cal =[]
    for x in a:
        cal.append(datetime.datetime.strftime(x,'%Y-%m-%d'))
    return cal

cal=get_calendar()


# In[2]:


data = pd.DataFrame()
for year in range(2015,2025):
    with open(f'Tools/NDX_data/NDXdata{year}.pkl', 'rb') as file:
        ndxData = pickle.load(file)
    data=pd.concat([data,ndxData])

data = data.loc[~data.index.duplicated(keep='last')]


# In[3]:


def getDate(date):
    #date needs to be a string like 2024-01-01
    dateList= date.split('-')
    return datetime.date(int(dateList[0]),int(dateList[1]),int(dateList[2]) )


# In[4]:





# In[ ]:


def getPrice(date, ticker, Open_Close="Close"):
    return data.loc[date,ticker][Open_Close]


# In[ ]:


def getDateOffset(Date,offset=0,cal=cal):
    try:
        return cal[cal.index(Date)+offset]
    except:
        cal=get_calendar()
        return cal[cal.index(Date)+offset]


# In[ ]:


def get_NDXmembers(year):
    file=f"Tools/NDX_data/Nasdaq100MembersJan{year}.csv"
    df = pd.read_csv(file,header = None)
    df.columns = ['members']
    NDX_members=[]
    for x in df['members']:
        ticker = x[:x.find(" ")]
        NDX_members.append(ticker)
    return NDX_members


# In[ ]:


def getPctChange(ticker,startDate,endDate,startTime="Close",endTime="Close"):
    startPrice = data.loc[startDate,ticker][startTime]
    endPrice = data.loc[endDate,ticker][endTime]
    pctChange = (endPrice-startPrice)/startPrice
    return pctChange


# In[ ]:


def getMomentum(date,ticker,debug=False):
    #a=getPctChange(ticker,getDateOffset(date,-5),getDateOffset(date,-4))
    #b=getPctChange(ticker,getDateOffset(date,-4),getDateOffset(date,-3))
    c=getPctChange(ticker,getDateOffset(date,-3),getDateOffset(date,-2))
    d=getPctChange(ticker,getDateOffset(date,-2),getDateOffset(date,-1))


   # delta_1 = (b-a)/(c-b)
    #delta_2 = (c-b)/(d-c)
    #momentum = delta_1/delta_2
    if debug:
        print(f"A:{a}\nB:{b}\nC:{c}\nD:{d}\n")
        print(f"Delta_1:{delta_1}\nDelta_2:{delta_2}\nMomentum:{momentum}")
    #return momentum

    return d/c


# In[ ]:


def get_SortedPctChange(InputDate, TimeInput=5,debug=False):

    NDX_members = get_NDXmembers(getDate(InputDate).year)
    PctChangeList = {"Ticker":[],"PctChange":[]}
    startDate = getDateOffset(InputDate,-TimeInput)
    endDate = getDateOffset(InputDate,-1)
    for ticker in NDX_members:
        try:
            pctChange = getPctChange(ticker,startDate,endDate)
            PctChangeList['Ticker'].append(ticker)
            PctChangeList['PctChange'].append(pctChange)

            if debug:
                print("---",ticker,"----")
                print(f"Percent Change: {pctChange}")
        except:
            i=1
            #print("UNABLE TO FIND:---",ticker,"----")

    #Convert to dataframe and sort it
    dfChange = (pd.DataFrame(PctChangeList).sort_values('PctChange',ascending=False)).reset_index(drop=True)

    return dfChange


# In[ ]:


def getShortReturns(RunDate,ShortStockList,holdTime=0,debug=False,stopLoss=-0.01):
    ShortReturnList = list()
    endDate = getDateOffset(RunDate,holdTime)
    for ticker in ShortStockList:
        try:


            #Get the data based on the provided ticker, RunDate, and startDate(being runDate-Timeinput)
            endPrice = getPrice(endDate,ticker,"Close")
            startPrice = getPrice(RunDate,ticker,"Open")
            runHighPrice= getPrice(RunDate,ticker,"High")

            Return = -(endPrice-startPrice)/startPrice
            #Checking For Stop Loss

            if -(runHighPrice-startPrice)/startPrice <= stopLoss:
                Return = stopLoss

            #Calculate and Append Return
            ShortReturnList.append(Return)

            if debug:
                print("---",ticker,"----")

                print(f"Start Date:{RunDate} , Start Price:{startPrice} ")
                print(f"End Date:{endDate} , End Price:{endPrice} ")
                print(f"Return:{Return}")
                print("")

        except:

            print("FAILED TO CALCULATE SHORT RETURN::---",ticker,"---",endDate)
           


    return ShortReturnList


# In[ ]:


def getLongReturns(RunDate,LongStockList,stopLoss = -0.01, holdTime=0,debug=False):
    LongReturnList = list()
    endDate = getDateOffset(RunDate,holdTime)

    for ticker in LongStockList:
        try:
            #Get the data based on the provided ticker, RunDate, and startDate(being runDate-Timeinput)
            endPrice = getPrice(endDate,ticker,"Close")
            startPrice = getPrice(RunDate,ticker,"Open")
            #Checking For Stop Loss
            runLowPrice= getPrice(endDate,ticker,"Low")
            Return = (endPrice-startPrice)/startPrice

            if (runLowPrice-startPrice)/startPrice <= stopLoss:
                Return = stopLoss


            #Calculate and Append Return

            LongReturnList.append(Return)


            if debug:
                print("---",ticker,"----")
                print(f"Start Date:{RunDate} , Start Price:{startPrice} ")
                print(f"End Date:{endDate} , End Price:{endPrice} ")
                print(f"Return:{Return}")
                print("")


        except:
            print("FAILED TO CALCULATE LONG RETURN:---",ticker,"--",endDate)
           

    return LongReturnList




def pick_trade(RunDate,NumStocks,stopLoss=-0.01,holdTime=0,TimeInput=5,debug=False):
    #Calculate pct change
    PctChange = get_SortedPctChange(RunDate,TimeInput,debug=debug)

    #select first N stocks and caculate percent retruns
    LongStockList = PctChange["Ticker"].iloc[:NumStocks]
    LongReturns = getLongReturns(RunDate,LongStockList,stopLoss=stopLoss,holdTime=holdTime,debug=debug)

    #select bottom N stocks and caculate percent retruns
    ShortStockList = PctChange["Ticker"].iloc[len(PctChange["Ticker"])-NumStocks:]
    ShortReturns = getShortReturns(RunDate,ShortStockList,stopLoss=stopLoss,holdTime=holdTime,debug=debug)
    TotalReturn = sum(LongReturns) / NumStocks + sum(ShortReturns) / NumStocks
   # print(f"Date:{RunDate}, Long Stocks:{list(LongStockList)}, Short Stocks:{list(ShortStockList)}, Return:{TotalReturn}\n")
    return TotalReturn


# In[ ]:


#PctChange = get_SortedPctChange('2024-10-09',4,debug=True)


# In[ ]:


#PctChange


# In[ ]:


#LongStockList = PctChange["Ticker"].iloc[:2]
#LongReturns = getLongReturns('2024-10-09',LongStockList,debug=True)


# In[ ]:


#LongReturns


# In[ ]:
