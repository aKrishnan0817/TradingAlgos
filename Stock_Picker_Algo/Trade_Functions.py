#!/usr/bin/env python
# coding: utf-8

# In[157]:


import pandas as pd
import pandas_market_calendars as mcal
import datetime
import yfinance as yf
import pickle


# In[158]:


with open('joinedData.pkl', 'rb') as file:
    data = pickle.load(file)


# In[159]:


def getDate(date):
    #date needs to be a string like 2024-01-01
    dateList= date.split('-')
    return datetime.date(int(dateList[0]),int(dateList[1]),int(dateList[2]) )


# In[160]:


def get_calendar():
    nyse = mcal.get_calendar('NYSE')
    a = nyse.valid_days(start_date='2019-01-01', end_date='2024-11-08')
    cal =[]
    for x in a:
        cal.append(datetime.datetime.strftime(x,'%Y-%m-%d'))
    return cal


# In[161]:


def get_NDXmembers(file="Nasdaq100MembersJan2024.csv"):
    df = pd.read_csv(file,header = None)
    df.columns = ['members']
    NDX_members=[]
    for x in df['members']:
        ticker = x[:x.find(" ")]
        NDX_members.append(ticker)
    return NDX_members
    


# In[174]:


def get_SortedPctChange(InputDate, TimeInput=5,NDXfile="Nasdaq100MembersJan2024.csv",debug=False):
    
    cal = get_calendar()
    NDX_members = get_NDXmembers(NDXfile)
    PctChangeList = {"Ticker":[],"PctChange":[]}
    startDate = cal[cal.index(InputDate)-TimeInput]
    InputDate = cal[cal.index(InputDate)-1]

    for ticker in NDX_members:
        try:
            #Get the data based on the provided ticker, RunDate, and startDate(being runDate-Timeinput)
            #Get the Close Values
            endPrice = data.loc[getDate(InputDate),ticker]["Close"]
            startPrice = data.loc[getDate(startDate),ticker]["Close"]
            
            

            #Calculaute the percent change in Close Price from RunDate and RunDate-TimeInput
            pctChange = (endPrice-startPrice)/startPrice

            PctChangeList['Ticker'].append(ticker)
            PctChangeList['PctChange'].append(pctChange)
            
            if debug:
                print("---",ticker,"----")

                print(f"Start Date:{startDate} , Start Price:{startPrice} ")
                print(f"End Date:{InputDate} , End Price:{endPrice} ")
                print(f"Percent Change: {pctChange}")
                print("")
        except:
            print("UNABLE TO FIND:---",ticker,"----")
        
    #Convert to dataframe and sort it 
    dfChange = (pd.DataFrame(PctChangeList).sort_values('PctChange',ascending=False)).reset_index(drop=True)
    
    return dfChange


# In[175]:


#get_SortedPctChange('2024-05-03',debug=True)


# In[ ]:





# In[145]:


def getShortReturns(RunDate,ShortStockList,holdTime=0,debug=False):
    ShortReturnList = list()
    cal = get_calendar()
    
    for ticker in ShortStockList:
        try:
            endDate = cal[cal.index(RunDate)+holdTime]

            #Get the data based on the provided ticker, RunDate, and startDate(being runDate-Timeinput)

            endPrice = data.loc[getDate(endDate),ticker]["Close"]
            startPrice = data.loc[getDate(RunDate),ticker]["Open"]

            
            #Calculate and Append Return
            Return = -(endPrice-startPrice)/startPrice
            ShortReturnList.append(Return)
            
            if debug:
                print("---",ticker,"----")

                print(f"Start Date:{RunDate} , Start Price:{startPrice} ")
                print(f"End Date:{endDate} , End Price:{endPrice} ")
                print(f"Return:{Return}")
                print("")
                
        except:
            print("UNABLE TO FIND:---",ticker,"----")

    return ShortReturnList


# In[220]:


def getLongReturns(RunDate,LongStockList,holdTime=0,debug=False):
    LongReturnList = list()
    cal = get_calendar()
    
    for ticker in LongStockList:  
        try:
            endDate = cal[cal.index(RunDate)+holdTime]
            
            #Get the data based on the provided ticker, RunDate, and startDate(being runDate-Timeinput)
            endPrice = data.loc[getDate(endDate),ticker]["Close"]
            startPrice = data.loc[getDate(RunDate),ticker]["Open"]
            
            #Calculate and Append Return
            Return = (endPrice-startPrice)/startPrice
            LongReturnList.append(Return)
            
            if debug:
                print("---",ticker,"----")

                print(f"Start Date:{RunDate} , Start Price:{startPrice} ")
                print(f"End Date:{endDate} , End Price:{endPrice} ")
                print(f"Return:{Return}")
                print("")

            
        except:
            print("UNABLE TO FIND:---",ticker,"----")
        
    return LongReturnList


# In[223]:


#PctChange = get_SortedPctChange('2024-10-09',4,debug=True)


# In[224]:


#PctChange


# In[225]:


#LongStockList = PctChange["Ticker"].iloc[:2]
#LongReturns = getLongReturns('2024-10-09',LongStockList,debug=True)


# In[226]:


#LongReturns


# In[ ]:




