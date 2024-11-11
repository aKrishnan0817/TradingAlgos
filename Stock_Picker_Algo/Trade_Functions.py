#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pandas_market_calendars as mcal
import datetime
import yfinance as yf


# In[ ]:


def get_calendar():
    nyse = mcal.get_calendar('NYSE')
    a = nyse.valid_days(start_date='2024-01-01', end_date='2024-11-08')
    cal =[]
    for x in a:
        cal.append(datetime.datetime.strftime(x,'%Y-%m-%d'))
    return cal


# In[11]:


def get_NDXmembers(file="Nasdaq100MembersJan2024.csv"):
    df = pd.read_csv(file,header = None)
    df.columns = ['members']
    NDX_members=[]
    for x in df['members']:
        ticker = x[:x.find(" ")]
        NDX_members.append(ticker)
    return NDX_members
    


# In[47]:


def get_SortedPctChange(InputDate, TimeInput=5,NDXfile="Nasdaq100MembersJan2024.csv"):
    
    cal = get_calendar()
    NDX_members = get_NDXmembers(NDXfile)
    PctChangeList = {"Ticker":[],"PctChange":[]}
    startDate = cal[cal.index(InputDate)-TimeInput]
    
    for ticker in NDX_members:
        
        #Get the data based on the provided ticker, RunDate, and startDate(being runDate-Timeinput)
        data = (yf.download(ticker, start=startDate, end=InputDate,multi_level_index=False)).reset_index()
        
        #Get the Close Values
        CloseVals=data["Close"].values
        
        #Calculaute the percent change in Close Price from RunDate and RunDate-TimeInput
        pctChange = (CloseVals[-1]-CloseVals[0])/CloseVals[0]
        
        PctChangeList['Ticker'].append(ticker)
        PctChangeList['PctChange'].append(pctChange)
        
    #Convert to dataframe and sort it 
    dfChange = (pd.DataFrame(PctChangeList).sort_values('PctChange',ascending=False)).reset_index(drop=True)
    
    return dfChange


# In[ ]:


def getLongReturns(RunDate,LongStockList,holdTime=1):
    LongReturnList = list()
    cal = get_calendar()
    
    for ticker in LongStockList:
        
        endDate = cal[cal.index(RunDate)+holdTime]

        #Get the data based on the provided ticker, RunDate, and startDate(being runDate-Timeinput)
        data = (yf.download(ticker, start=RunDate, end=endDate,multi_level_index=False)).reset_index()
        
        #Get the Close and Open Values
        ClosePrice=data["Close"].values
        OpenPrice = data['Open'].values
        
        #Calculate and Append Return
        Return = (ClosePrice[-1]-OpenPrice[0])/OpenPrice[0]
        LongReturnList.append(Return)
    return LongReturnList


# In[ ]:


def getShortReturns(RunDate,ShortStockList,holdTime=1):
    ShortReturnList = list()
    cal = get_calendar()
    
    for ticker in ShortStockList:
        
        endDate = cal[cal.index(RunDate)+holdTime]

        #Get the data based on the provided ticker, RunDate, and startDate(being runDate-Timeinput)
        data = (yf.download(ticker, start=RunDate, end=endDate,multi_level_index=False)).reset_index()
        
        #Get the Close and Open Values
        ClosePrice=data["Close"].values
        OpenPrice = data['Open'].values
        
        #Calculate and Append Return
        Return = -(ClosePrice[-1]-OpenPrice[0])/OpenPrice[0]
        ShortReturnList.append(Return)
    return ShortReturnList


# In[ ]:




