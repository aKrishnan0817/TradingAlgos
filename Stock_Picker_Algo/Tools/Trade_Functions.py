#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import pandas_market_calendars as mcal
import datetime
import yfinance as yf
import pickle
import os


# In[ ]:


os.chdir('../')


# In[ ]:


def get_calendar():
    nyse = mcal.get_calendar('NYSE')
    a = nyse.valid_days(start_date='2014-01-01', end_date='2024-11-14')
    cal =[]
    for x in a:
        cal.append(datetime.datetime.strftime(x,'%Y-%m-%d'))
    return cal


# In[ ]:


cal=get_calendar()


# In[ ]:


data = pd.DataFrame()
for year in range(2015,2025):
    with open(f'Tools/NDX_data/NDXdata{year}.pkl', 'rb') as file:
        ndxData = pickle.load(file)
    data=pd.concat([data,ndxData])

data = data.loc[~data.index.duplicated(keep='last')]


# In[ ]:


def getDate(date):
    #date needs to be a string like 2024-01-01
    dateList= date.split('-')
    return datetime.date(int(dateList[0]),int(dateList[1]),int(dateList[2]) )


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


def get_deltaPctChange(date,ticker,debug=False):
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
            print("UNABLE TO FIND:---",ticker,"----")
        
    #Convert to dataframe and sort it 
    dfChange = (pd.DataFrame(PctChangeList).sort_values('PctChange',ascending=False)).reset_index(drop=True)
    
    return dfChange


# In[ ]:





# In[ ]:


prices = data.loc["2024-01-04":"2024-01-09","AAPL"]
prices


# In[ ]:


prices.index[3]


# In[ ]:


def getReturn_withStopLoss(runDate,endDate,ticker,holdTime,stopLoss,long_short):
    s=1
    if long_short == "Long": 
        K = "Low"
    if long_short == "Short": 
        K= "High"
        s=-1
    prices = list(data.loc[runDate:endDate,ticker])
    price = data.loc[runDate:endDate,ticker]
    
    for day in range(len(prices)):
        if s*(prices[day][K] - prices[day]["Open"])/prices[day]["Open"] <= stopLoss:
            Return = -0.0004 + stopLoss
            return Return , price.index[day],1
        try:
            if s*(prices[day]["Close"]- prices[day+1]["Open"] )/prices[day]["Close"] <= stopLoss:
                Return = -0.0004 + s*((prices[day+1]["Open"] - prices[0]["Open"])/prices[0]["Open"])
                return Return ,price.index[day+1],1
        except:
            Return = -0.0004 + s*((prices[-1]["Close"] - prices[0]["Open"])/prices[0]["Open"])
            return Return ,price.index[-1],0
   


# In[ ]:


#PctChange = get_SortedPctChange('2024-10-09',4,debug=False)
#getShortReturns('2024-10-09',PctChange["Ticker"][:3],holdTime=5)


# In[ ]:


def getLongReturns(RunDate,LongStockList,stopLoss = -0.01, holdTime=0,debug=False):
    LongReturnList = list()
    endDate = getDateOffset(RunDate,holdTime)
    CloseDates=list()
    stopLosses= list()
    for ticker in LongStockList:
        try:
            
            Return,closeDate,stopLossFlag= getReturn_withStopLoss(RunDate,endDate,ticker,holdTime,stopLoss,long_short="Long")
            LongReturnList.append(Return)
            CloseDates.append(closeDate)
            stopLosses.append(stopLossFlag)

        except:
            print("FAILED TO CALCULATE LONG RETURN:---",ticker,"--",endDate)
            LongReturnList.append(-0.0004)
    x = len(LongStockList)
    return pd.DataFrame({"Type":["Long"]*x, "ExecutionDate":[RunDate]*x, "CloseDate":CloseDates,"Returns":LongReturnList,"StopLoss":stopLosses})




# In[ ]:


def getShortReturns(RunDate,ShortStockList,holdTime=0,debug=False,stopLoss=-0.01):
    ShortReturnList = list()
    CloseDates=list()
    stopLosses= list()

    endDate = getDateOffset(RunDate,holdTime)
    for ticker in ShortStockList:
        try:
            Return,trade,stopLossFlag = getReturn_withStopLoss(RunDate,endDate,ticker,holdTime,stopLoss,long_short="Short")
            CloseDates.append(trade)
            stopLosses.append(stopLossFlag)
            ShortReturnList.append(Return)

        except:
            print("FAILED TO CALCULATE SHORT RETURN::---",ticker,"---",endDate)
            ShortReturnList.append(-0.0004)
           

    x = len(ShortStockList)
    return pd.DataFrame({"Type":["Short"]*x,"ExecutionDate":[RunDate]*len(ShortStockList), "CloseDate":CloseDates,"Returns":ShortReturnList,"StopLoss":stopLosses})


# In[ ]:


def calculate_mdd(return_vals):
    # Calculate the cumulative returns (wealth index)
    wealth_index = (1 + return_vals).cumprod()
    
    # Calculate the running maximum
    running_max = wealth_index.cummax()
    
    # Calculate drawdowns (difference between running max and current value)
    drawdowns = (wealth_index - running_max) / running_max
    
    # The maximum drawdown is the largest negative drawdown (i.e., most significant loss)
    mdd = drawdowns.min()  # This will give the maximum drawdown (most negative value)
    
    return mdd

def calculate_sortino_ratio(return_vals, risk_free_rate=0.05):
    # Calculate the excess returns over the risk-free rate
    excess_returns = return_vals - risk_free_rate / 252  # Convert annual risk-free rate to daily
    
    # Calculate downside deviation (negative returns only)
    downside_returns = excess_returns[excess_returns < 0]  # Only consider negative returns
    downside_deviation = np.std(downside_returns)  # Standard deviation of negative returns
    
    # Calculate the mean of excess returns
    mean_excess_return = np.mean(excess_returns)
    
    # Calculate the Sortino ratio (avoid division by zero if downside deviation is zero)
    if downside_deviation == 0:
        sortino_ratio = np.nan  # Return NaN if no downside deviation (e.g., no negative returns)
    else:
        sortino_ratio = mean_excess_return / downside_deviation
    
    return sortino_ratio


# In[ ]:


def yearly_plots(returnDf):
    """
    Saves a plot for each year in the range start_year to end_year.
    
    Args:
    - dataframe (pd.DataFrame): The DataFrame containing the data.
    - start_year (int): The starting year (inclusive).
    - end_year (int): The ending year (inclusive).
    - column_to_plot (str): The column to plot (e.g., 'ReturnVals').
    - date_column (str): The column containing dates (e.g., 'Date').
    
    Returns:
    - None
    """
    # Ensure the date column is in datetime format
    
    for year in range(2015, 2025 ):
        # Filter data for the specific year
        yearly_data = returnDf[returnDf["Date"].dt.year == year]
        
        if not yearly_data.empty:  # Only create plots for years with data
            plt.figure(figsize=(10, 5))
            plt.plot(
                yearly_data["Date"],
                yearly_data["ReturnVals"],
                label=f"{year}",
                color="blue"
            )
            plt.title(f"Retruns - {year}")
            plt.xlabel("Date")
            plt.ylabel("Returns")
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.6)
            
            # Save the plot
            plt.savefig(f"Visulizations/returns_{year}.png", dpi=300, bbox_inches='tight')
            plt.close()

# Example Usage:
# save_yearly_plots_simple(returnDf, 2015, 2024, 'ReturnVals', 'Date')


# In[ ]:




