import pandas as pd
import numpy as np
import pandas_market_calendars as mcal
import datetime
import yfinance as yf
import pickle
import os
import matplotlib.pyplot as plt

def get_calendar(startDate='2014-01-01',endDate='2024-11-14'):
    nyse = mcal.get_calendar('NYSE')
    a = nyse.valid_days(start_date=startDate, end_date=endDate)
    cal =[]
    for x in a:
        cal.append(datetime.datetime.strftime(x,'%Y-%m-%d'))
    return cal

def load_data(filePath="Tools/NDX_data/NDX_2015-2014.pkl"):
    with open(filePath, 'rb') as file:
        data = pickle.load(file)
    return data

class Tools:


    def __init__(self, holdTime, lookback,stopLoss,numStocks):
        self.holdTime = holdTime
        self.lookback = lookback
        self.stopLoss = stopLoss
        self.numStock = numStocks
        self.data = load_data()
        self.cal= get_calendar()

    
    
    def getDate(date):
        """ Takes a date in "yyyy-mm-dd" format  
            returns a DateTime object of same date """
        dateList= date.split('-')
        return datetime.date(int(dateList[0]),int(dateList[1]),int(dateList[2]) )
    
    def getPrice(self,date, ticker, pos="Close"):
        """Returns Price of stock at certain date
            pos is either open, close, low or high """
        return self.data.loc[date,ticker][pos]
    
    def getDateOffset(self, Date,offset=0):
        """Using the calendar of trading days find n(offset) days 
            after provided date (Date) """
        cal = self.cal
        return cal[cal.index(Date)+offset]
    
    def get_NDXmembers(year):
        """Since new members can be added and removed from the index
            while back testing, for each year, we must ensure we are 
            using the correct members. This extracts the members from
            a csv containing them 
        """
        df = pd.read_csv(f"Tools/NDX_data/Nasdaq100MembersJan{year}.csv",header = None)
        df.columns = ['members']
        NDX_members=[]
        for x in df['members']:
            ticker = x[:x.find(" ")]
            NDX_members.append(ticker)
        return NDX_members
    
    def getPctChange(self,ticker,startDate,endDate,startTime="Close",endTime="Close"):
        """ For a given stock(ticker) calculate the percent change
            between the start and endDate
        """
        startPrice = self.data.loc[startDate,ticker][startTime]
        endPrice = self.data.loc[endDate,ticker][endTime]
        pctChange = (endPrice-startPrice)/startPrice
        return pctChange

    def get_SortedPctChange(self,InputDate):

        """ Based on the Input Date(day_N) finds the
            Percentage Change of all stocks currently
            in the index betwee day_N-1 and day_N-lookback
            
            It then sorts the list and returns a dataFrame.
        """
        
        NDX_members = self.get_NDXmembers(self.getDate(InputDate).year)
        PctChangeList = {"Ticker":[],"PctChange":[]}
        startDate = self.getDateOffset(InputDate,-self.lookback)
        endDate = self.getDateOffset(InputDate,-1)
        for ticker in NDX_members:
            try:     
                pctChange = self.getPctChange(ticker,startDate,endDate)
                PctChangeList['Ticker'].append(ticker)
                PctChangeList['PctChange'].append(pctChange)
            except:
                i=1            
        #Convert to dataframe and sort it 
        dfChange = (pd.DataFrame(PctChangeList).sort_values('PctChange',ascending=False)).reset_index(drop=True)
        
        return dfChange
    
    def getReturn_withStopLoss(self,runDate,endDate,ticker,long_short):
        """ For holding periods > 1 
            it checks( i = 0, inititally)
            pctChange between day_N open and day_N+i low
            then checks 
            pctChange between day_N open and day_N+(i+1) open
            
            if pctChange is ever less than stopLoss, CLOSE OUT
            otherwise returns the pctChange between day_N and day_N+holdtime

            s is simply a variable either 1 or -1, to adjust based on
            wether going long or short """
        s=1
        if long_short == "Long": 
            K = "Low"
        if long_short == "Short": 
            K= "High"
            s=-1

        prices = list(self.ata.loc[runDate:endDate,ticker])
        price = self.data.loc[runDate:endDate,ticker]
        putOnPrice= self.getPrice(runDate,ticker,"Open")

        for day in range(len(prices)):

            if s*(prices[day][K] - putOnPrice)/putOnPrice <= self.stopLoss:
                Return = -0.0004 + self.stopLoss
                return Return , price.index[day],1
            try:
                if s*(prices[day+1]["Open"]-putOnPrice)/putOnPrice <= self.stopLoss:
                    Return = -0.0004 + s*((prices[day+1]["Open"] - prices[0]["Open"])/prices[0]["Open"])
                    return Return ,price.index[day+1],1
            except:
                break
        Return = -0.0004 + s*((prices[-1]["Close"] -putOnPrice)/putOnPrice)
        return Return ,price.index[-1],0
        

    def getLongReturns(self,RunDate,LongStockList):
        """
        Takes in the day it should be ran, the stocks to go long on, the stop loss and how long to hold the stocks
        Calcultaes long returns and returns a dataframe of the trade infromation.
        The trade information includes each stock, when it bought it, when it closed out and the returns
        """
        LongReturnList = list()
        endDate = self.getDateOffset(RunDate,self.holdTime)
        CloseDates=list()
        stopLosses= list()
        for ticker in LongStockList:
            try:
                
                Return,closeDate,stopLossFlag= self.getReturn_withStopLoss(RunDate,endDate,ticker,long_short="Long")
                LongReturnList.append(Return)
                CloseDates.append(closeDate)
                stopLosses.append(stopLossFlag)

            except:
                #print("FAILED TO CALCULATE LONG RETURN:---",ticker,"--",endDate)
                LongReturnList.append(-0.0004)
                stopLosses.append(2)
                CloseDates.append(endDate)
        x = len(LongStockList)
        return pd.DataFrame({"Stock": LongStockList,"Type":["Long"]*x, "ExecutionDate":[RunDate]*x,"CloseDate":CloseDates,"Returns":LongReturnList,"StopLoss":stopLosses})


    def getShortReturns(self,RunDate,ShortStockList):
        """
        Takes in the day it should be ran, the stocks to go short on, the stop loss and how long to hold the stocks
        Calcultaes long returns and returns a dataframe of the trade infromation.
        The trade information includes each stock, when it bought it, when it closed out and the returns
        """
        ShortReturnList = list()
        CloseDates=list()
        stopLosses= list()

        endDate = self.getDateOffset(RunDate,self.holdTime)
        for ticker in ShortStockList:
            try:
                Return,trade,stopLossFlag = self.getReturn_withStopLoss(RunDate,endDate,ticker,long_short="Short")
                CloseDates.append(trade)
                stopLosses.append(stopLossFlag)
                ShortReturnList.append(Return)

            except:
                #print("FAILED TO CALCULATE SHORT RETURN::---",ticker,"---",endDate)
                ShortReturnList.append(-0.0004)
                stopLosses.append(2)
                CloseDates.append(endDate)
                

        x = len(ShortStockList)
        return pd.DataFrame({"Stock": ShortStockList,"Type":["Short"]*x,"ExecutionDate":[RunDate]*len(ShortStockList), "CloseDate":CloseDates,"Returns":ShortReturnList,"StopLoss":stopLosses})
    
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
                plt.tight_layout()

                plt.savefig(f"Visulizations/returns_{year}.png", dpi=300, bbox_inches='tight')
                plt.close()

    def pick_trade(self,TradeData,RunDate,NumStocks):
        #Calculate pct change
        
        PctChange = self.get_SortedPctChange(RunDate,self.lookback)
        
        #select first N stocks and caculate percent retruns
        LongStockList = PctChange["Ticker"].iloc[:NumStocks]
        LongTradeInfo = self.getLongReturns(RunDate,LongStockList)
        #select bottom N stocks and caculate percent retruns
        ShortStockList = PctChange["Ticker"].iloc[len(PctChange["Ticker"])-NumStocks:]
        ShortTradeInfo = self.getShortReturns(RunDate,ShortStockList)
        TotalReturn = sum(LongTradeInfo["Returns"]) / NumStocks + sum(ShortTradeInfo["Returns"]) / NumStocks
        
        return TotalReturn, pd.concat([TradeData,LongTradeInfo,ShortTradeInfo])

