#This algo tests Atul's ML output
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
# Lets read in SPY data

SPYdf = pd.read_csv("spydata.csv")
print(SPYdf.head())

for i in range(0,len(SPYdf)):
    SPYdf.loc[i,'Date'] = datetime.strptime(SPYdf.loc[i,'Date'],'%m/%d/%Y')



# Lets read in the output from the Predictor
rnnOut = pd.read_csv("rnnPrediction-1.csv")
print(rnnOut.head())

for i in range(0,len(rnnOut)):
    rnnOut.loc[i,'Date'] = datetime.strptime(rnnOut.loc[i,'Date'],'%m/%d/%Y')
print(rnnOut.head())

Date1 = rnnOut.iloc[0,0]
Date2 = rnnOut.loc[len(rnnOut)-1,'Date']
print(type(Date1))
print(Date1)
print(Date2)
SPYdf = SPYdf[(SPYdf['Date']>=Date1) & (SPYdf['Date']<=Date2)]
SPYdf = SPYdf.reset_index()
print(SPYdf.head())
print(SPYdf.iloc[len(SPYdf)-1])



# Test1: Lets do a simple test
# Lets see how effective the predictor data is on predicting trends

# This is time the trade is held
HoldTime = 3
# If at time to the predictor value for the next hold period is higher, we go long else we go short

ReturnList = list()
indexList = list()
PositionData = list()
for i in range(HoldTime,len(rnnOut),HoldTime):
    if rnnOut.loc[i,'Close'] - rnnOut.loc[i-HoldTime,'Close'] > 0:
        # Assumes we buy at the prior evening's close and take out at the next days close
        Return = (SPYdf.loc[i,'Close']-SPYdf.loc[i-HoldTime,'Close'])/SPYdf.loc[i-HoldTime,'Close']
        ReturnList.append(Return)
        indexList.append(i)
        for j in range(i-HoldTime,i):
            PositionData.append(1)
    else:
        # Go short
        Return = (-SPYdf.loc[i, 'Close'] + SPYdf.loc[i-HoldTime, 'Close']) / SPYdf.loc[i-HoldTime, 'Close']
        ReturnList.append(Return)
        indexList.append(i)
        for j in range(i-HoldTime,i):
            PositionData.append(-1)

fig = plt.figure()
plt.plot(ReturnList,'*')


print("Sum of all daily returns = ",sum(ReturnList))
print("Max daily return = ", max(ReturnList))
print("Min daily return = ", min(ReturnList))
CompRet = 1
CompRetList = list()
for i in range(0,len(ReturnList)):
    if i == 0:
        CompRet = (1+ReturnList[i])
    else:
        CompRet = CompRet * (1+ReturnList[i])
    CompRetList.append(CompRet)

fig = plt.figure()
plt.plot(CompRetList)



SPYReturnList = list()
AlgoReturnList = list()
print("Length of Position Data: ",len(PositionData))
print("Lenght of SPY: ", len(SPYdf))


for i in range(0,len(PositionData)-1):
    if PositionData[i] == 1:
        AlgoReturn = (SPYdf.loc[i+1,'Close']-SPYdf.loc[i,'Close'])/SPYdf.loc[i,'Close']
    else:
        AlgoReturn = (-SPYdf.loc[i + 1, 'Close'] + SPYdf.loc[i,'Close']) / SPYdf.loc[i,'Close']
    Return = (SPYdf.loc[i+1,'Close']-SPYdf.loc[i,'Close'])/SPYdf.loc[i,'Close']
    AlgoReturnList.append(AlgoReturn)
    SPYReturnList.append(Return)

CompRetAlgoList = list()
CompRetSPList = list()
CompRetAlgo = 1
CompRetSP = 1
for i in range(0,len(AlgoReturnList)):
    if i==0:
        CompRetAlgo = (1+AlgoReturnList[i])
    else:
        CompRetAlgo = CompRetAlgo * (1+AlgoReturnList[i])

    CompRetAlgoList.append(CompRetAlgo)

    if i == 0:
        CompRetSP = (1 + SPYReturnList[i])
    else:
        CompRetSP = CompRetSP * (1 + SPYReturnList[i])

    CompRetSPList.append(CompRetSP)


fig = plt.figure()
plt.plot(CompRetAlgoList,'r')
plt.plot(CompRetSPList,'b')

plt.show()













