import matplotlib.pyplot as plt
import pandas as pd
import pandas_market_calendars as mcal
import datetime
from Tools.Trade_Functions import *
import numpy as np
import mlflow
import optuna

def getLongReturns(RunDate,LongStockList,stopLoss = -0.01, holdTime=0,debug=False,numDaysToCheckStopLoss=5):
    LongReturnList = list()
    endDate = getDateOffset(RunDate,holdTime)
    CloseDates=list()
    stopLosses= list()
    for ticker in LongStockList:
        try:
            putOnPrice = getPrice(RunDate,ticker,"Open")
            firstDayLow = getPrice(RunDate,ticker,"Low")

            if (firstDayLow-putOnPrice)/putOnPrice <= stopLoss:
                Return = stopLoss
                closeDate=RunDate
                stopLossFlag=1
            else:
                Return = (getPrice(endDate,ticker,"Close")-putOnPrice)/putOnPrice
                closeDate=endDate
                stopLossFlag=0

            LongReturnList.append(Return-0.0004)
            CloseDates.append(closeDate)
            stopLosses.append(stopLossFlag)

        except:
            #print("FAILED TO CALCULATE LONG RETURN:---",ticker,"--",endDate)
            LongReturnList.append(-0.0004)
            stopLosses.append(2)
            CloseDates.append(endDate)
    x = len(LongStockList)
    return pd.DataFrame({"Stock": LongStockList,"Type":["Long"]*x, "ExecutionDate":[RunDate]*x,"CloseDate":CloseDates,"Returns":LongReturnList,"StopLoss":stopLosses})




# In[ ]:


def getShortReturns(RunDate,ShortStockList,holdTime=0,debug=False,stopLoss=-0.01,numDaysToCheckStopLoss=5):
    ShortReturnList = list()
    CloseDates=list()
    stopLosses= list()

    endDate = getDateOffset(RunDate,holdTime)
    for ticker in ShortStockList:
        try:
            putOnPrice = getPrice(RunDate,ticker,"Open")
            firstDayHigh = getPrice(RunDate,ticker,"High")

            if -(firstDayHigh-putOnPrice)/putOnPrice <= stopLoss:
                Return = stopLoss
                closeDate=RunDate
                stopLossFlag=1
            else:
                Return = -(getPrice(endDate,ticker,"Close")-putOnPrice)/putOnPrice
                closeDate=endDate
                stopLossFlag=0

            LongReturnList.append(Return-0.0004)
            CloseDates.append(closeDate)
            stopLosses.append(stopLossFlag)

        except:
            #print("FAILED TO CALCULATE SHORT RETURN::---",ticker,"---",endDate)
            ShortReturnList.append(-0.0004)
            stopLosses.append(2)
            CloseDates.append(endDate)


    x = len(ShortStockList)
    return pd.DataFrame({"Stock": ShortStockList,"Type":["Short"]*x,"ExecutionDate":[RunDate]*len(ShortStockList), "CloseDate":CloseDates,"Returns":ShortReturnList,"StopLoss":stopLosses})

def pick_trade(TradeData,RunDate,NumStocks,stopLoss=-0.01,holdTime=0,TimeInput=5,debug=False,numDaysToCheckStopLoss=5):
    #Calculate pct change

    PctChange = get_SortedPctChange(RunDate,TimeInput,debug=False)

    #select first N stocks and caculate percent retruns
    LongStockList = PctChange["Ticker"].iloc[:NumStocks]
    LongTradeInfo = getLongReturns(RunDate,LongStockList,stopLoss=stopLoss,holdTime=holdTime,debug=debug,numDaysToCheckStopLoss=5)
    #select bottom N stocks and caculate percent retruns
    ShortStockList = PctChange["Ticker"].iloc[len(PctChange["Ticker"])-NumStocks:]
    ShortTradeInfo = getShortReturns(RunDate,ShortStockList,stopLoss=stopLoss,holdTime=holdTime,debug=debug,numDaysToCheckStopLoss=5)
    TotalReturn = sum(LongTradeInfo["Returns"]) / NumStocks + sum(ShortTradeInfo["Returns"]) / NumStocks

    return TotalReturn, pd.concat([TradeData,LongTradeInfo,ShortTradeInfo])


experiment_counter=0
mlflow.set_experiment("Momentum Rider Tuning:V6")
framedCal= get_calendar()


def objective(trial):
    global experiment_counter
    expirement_name = f"Expirement {experiment_counter}"

    with mlflow.start_run(run_name=expirement_name) as run:
        #Setup Paramter Variation

        TimeInput = trial.suggest_int('TimeInput', 2, 7)
        NumStocks= trial.suggest_int('NumStocks', 2, 10)
        holdTime=trial.suggest_int('holdTime', 0, 7)
        stopLoss=trial.suggest_float('stopLoss',-0.05, -0.01)
        numDaysToCheckStopLoss= holdTime#trial.suggest_int('numDaysToCheckStopLoss', 1, holdTime)#must be less than holdtime
        TradeData=pd.DataFrame()



        #Date Range
        cal=list()
        DateRange = [None,None]
        for i in range(0,len(framedCal),holdTime+1):
            if DateRange[0]==None and framedCal[i].startswith(str(2015)):
                DateRange[0]=framedCal[i]
            if framedCal[i].startswith(str(2024)):
                DateRange[1]=framedCal[i]
            cal.append(framedCal[i])
        DateRange=[cal.index(DateRange[0]),cal.index(DateRange[1])]
        TotalReturnList=list()


        #Run Algorithim
        for day in cal[DateRange[0]:DateRange[1]]:
            dailyReturn,TradeData = pick_trade(TradeData,RunDate=day,NumStocks=NumStocks,stopLoss=stopLoss,TimeInput=TimeInput,holdTime=holdTime,debug=False,numDaysToCheckStopLoss=numDaysToCheckStopLoss)
            TotalReturnList.append(dailyReturn)
        TradeData=TradeData.reset_index(drop=True)
        returnDf = pd.DataFrame({'Date': pd.to_datetime(cal[DateRange[0]:DateRange[1]]),'Return':TotalReturnList})

        #Compound Retruns
        M = 1
        returnVal=[]
        for i in returnDf["Return"]:
            M = M*(1+i)
            returnVal.append(M)
        returnDf=pd.concat([returnDf,pd.DataFrame({"ReturnVals":returnVal})],axis=1)

        #Calculate Metrics
        SharpeRatio =(np.mean(returnDf["Return"]) * 252 - 0.05) / (np.std(returnDf["Return"]) * np.sqrt(252))
        CumulativeReturn = returnDf.loc[len(returnDf)-1,"ReturnVals"]
        max_drawdown = calculate_mdd(returnDf["Return"])
        sortino_ratio = calculate_sortino_ratio(returnDf["Return"])


        pLratio = len(returnDf["Return"][returnDf["Return"]>0])/ len(returnDf["Return"])

        avg_loss= np.mean(returnDf["Return"][returnDf["Return"]<0])
        avg_prof= np.mean(returnDf["Return"][returnDf["Return"]>0])



        #Saving A plot
        plt.figure(figsize=(15, 6))  # Set the figure size
        plt.plot(returnDf['Date'], returnDf['ReturnVals'],  linestyle='-', color='blue', label="Return Vals")
        plt.title("Return Values Over Time", fontsize=16)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Return Vals", fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=12)
        plt.tight_layout()
        plt.savefig("Visulizations/returns.png", dpi=300, bbox_inches='tight')
        plt.close()
        #LOG Paramters, Metrics and Artifacts

        mlflow.log_param("TimeInput", trial.params['TimeInput'])
        mlflow.log_param("NumStocks", trial.params['NumStocks'])
        mlflow.log_param("holdTime", trial.params['holdTime'])
        mlflow.log_param("stopLoss", trial.params['stopLoss'])
      #  mlflow.log_param("numDaysToCheckStopLoss", trial.params['numDaysToCheckStopLoss'])


        mlflow.log_metric("CumulativeReturn", CumulativeReturn)
        mlflow.log_metric("SharpeRatio", SharpeRatio)
        mlflow.log_metric("Profit_Loss_Ratio", pLratio)
        mlflow.log_metric("avg_prof",avg_prof)
        mlflow.log_metric("avg_loss", avg_loss)

        mlflow.log_metric("Max_Draw_Down",max_drawdown)
        mlflow.log_metric("sortino_ratio",sortino_ratio)


        yearly_plots(returnDf)

        mlflow.log_artifact("Visulizations/returns.png", artifact_path="Visulizations")


        yearlyReturns=list()
        years=range(2015,2025)

        for year in range(2015,2025):
            returnDf_year = returnDf[returnDf['Date'].dt.year == year]
            returnDf_year.loc[:, 'Return'] = returnDf_year['Return'].astype(float)
            yearlyReturns.append(np.prod(1 + returnDf_year['Return']))
            mlflow.log_artifact(f"Visulizations/returns_{year}.png", artifact_path="Visulizations")

        plt.figure(figsize=(10, 6))
        plt.plot(years, yearlyReturns, marker='o', linestyle='-', color='blue', label='Annual Returns')

        # Add numeric values above each point
        for i, value in enumerate(yearlyReturns):
            plt.text(years[i], value, f'{value:.2f}', ha='center', va='bottom', fontsize=10)

        # Add labels, title, and grid
        plt.title("Annual Returns (2015-2024)", fontsize=16)
        plt.xlabel("Year", fontsize=12)
        plt.ylabel("Return Value", fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=12)
        plt.tight_layout()
        # Save the plot as PNG
        plt.savefig("Visulizations/annual_returns.png", dpi=300)
        plt.close()

        mlflow.log_artifact("Visulizations/annual_returns.png", artifact_path="Visulizations")

        TradeData.to_csv("Visulizations/TradeData.csv")
        returnDf.to_csv("Visulizations/Returns.csv")
        mlflow.log_artifact("Visulizations/TradeData.csv", artifact_path="Generated_Data")
        mlflow.log_artifact("Visulizations/Returns.csv", artifact_path="Generated_Data")





        experiment_counter += 1

        return CumulativeReturn, SharpeRatio



study = optuna.create_study(directions=["maximize","maximize"])
study.optimize(objective, n_trials=3000)
