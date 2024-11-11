import pandas as pd
import time
from datetime import datetime
import pickle

class Trader:
    def __init__(self):
        self.tradeData = pd.DataFrame(dict(Position = [],TradePrice = [], TradeTime = [], Method=[]))

    def goLong(self,currTimeRow, MOT = None):
        price = currTimeRow["price"]
        time = currTimeRow["Time2"]
        self.tradeData = pd.concat([self.tradeData, pd.DataFrame([[1,price,time,MOT]], columns=self.tradeData.columns) ], ignore_index=True)

    def goShort(self,currTimeRow, MOT = None):
        price = currTimeRow["price"]
        time = currTimeRow["Time2"]
        self.tradeData = pd.concat([self.tradeData, pd.DataFrame([[-1,price,time,MOT]], columns=self.tradeData.columns) ], ignore_index=True)

    def closeOut(self,currTimeRow, MOT = None):
        price = currTimeRow["price"]
        time = currTimeRow["Time2"]
        self.tradeData = pd.concat([self.tradeData, pd.DataFrame([[0,price,time,MOT]], columns=self.tradeData.columns) ], ignore_index=True)

    def getTradeData(self):
        return self.tradeData

    def getReturnList(self,contractValue=50):
        ReturnList =[]
        for i in range(0,len(self.tradeData)):
            if self.tradeData.loc[i,'Position'] == -1:
                ReturnList.append((self.tradeData.loc[i,'TradePrice']-self.tradeData.loc[i+1,'TradePrice'])*contractValue)
            elif self.tradeData.loc[i,'Position'] == 1:
                ReturnList.append((self.tradeData.loc[i + 1, 'TradePrice']-self.tradeData.loc[i, 'TradePrice'])*contractValue)
        return ReturnList

    def getLastTradePos(self):
        if len(self.tradeData) == 0:
            return 0
        return self.tradeData.loc[len(self.tradeData)-1,"Position"]

    def getLastTradePrice(self):
        return self.tradeData.loc[len(self.tradeData)-1,"TradePrice"]

    def getLR(self):
        rdf= pd.DataFrame(self.getReturnList())
        return rdf[rdf<0].count() / (len(rdf)-rdf[rdf==0].count())

    def getTradeInfo(self,contractValue=50):
        ReturnList = self.getReturnList(contractValue)
        return {"Total Return" :sum(ReturnList),
                "Max Return" : max(ReturnList),
                "Min Return" : min(ReturnList)}
