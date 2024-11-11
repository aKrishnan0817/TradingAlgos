import pandas as pd
import time
from datetime import datetime
import pickle

class AlgoTools:
    def __init__(self,tickData):
        self.tickData = tickData
        #self.startTime = startTime
        #self.endTime = endTime
        self.tradeData = pd.DataFrame(dict(Position = [],TradePrice = [], TradeTime = []))


    #Current Time is not an actual time but rather the nth data point which corresponds to some time
    def getPriceDelta(self,currTime):
        return self.tickData.loc[currTime,"price"]-self.tickData.loc[currTime-1,"price"]

    def getTimeDelta(self,currTime):
        timeDiff = (self.tickData.loc[currTime,"Time2"]-self.tickData.loc[currTime-1,"Time2"]).total_seconds()
        if timeDiff ==0:
            return 1
        return timeDiff

    def getRate(self,currTime):
        return self.getPriceDelta(currTime) / self.getTimeDelta(currTime)

    def getAccel(self,currTime):
        return self.getRate(currTime)-self.getRate(currTime-1)/self.getTimeDelta(currTime)

    def checkNextDay(self,currTime):
        timeDiff = datetime.strptime(self.tickData.loc[currTime,"date"], '%m/%d/%Y').date() - datetime.strptime(self.tickData.loc[currTime-1,"date"], '%m/%d/%Y').date()
        return timeDiff.days >0

    def getData(self,startTime,endTime):
        startIndex = self.tickData[self.tickData.date == startTime].index[0]
        endIndex = self.tickData[self.tickData.date == endTime].index[-1] +1
        return self.tickData[startIndex:endIndex]
