import pandas as pd
from matplotlib import pyplot as plt
import statistics

df = pd.read_csv("ReturnLists.csv")
df.columns = ['0','SPYRet','AlgoRet']
df = df.drop('0', axis=1)
print(df.head())

print(df.shape)
print("Sum of Algo Rets: ", df['AlgoRet'].sum())
print("Sum of SPY Rets: ", df['SPYRet'].sum())

AlgoRetList = list()
for i in range(0,len(df)):
    AlgoRetList.append(df.loc[i,'AlgoRet'])



CompRetAlgoList = list()
CompRetSPList = list()
CompRetAlgo = 1
CompRetSP = 1
for i in range(0,len(df)):
    if i==0:
        CompRetAlgo = (1+df.loc[i,'AlgoRet'])
    else:
        CompRetAlgo = CompRetAlgo * (1+df.loc[i,'AlgoRet'])

    CompRetAlgoList.append(CompRetAlgo)

    if i == 0:
        CompRetSP = (1 + df.loc[i,'SPYRet'])
    else:
        CompRetSP = CompRetSP * (1 + df.loc[i,'SPYRet'])

    CompRetSPList.append(CompRetSP)


fig = plt.figure()
plt.plot(CompRetAlgoList,'r')
plt.plot(CompRetSPList,'b')

fig = plt.figure()
plt.plot(AlgoRetList,'*')
NumberofPositveRets = [i for i in AlgoRetList if i > 0]
NumberofNegativeRets = [i for i in AlgoRetList if i<=0]

PctofSuccess = len(NumberofPositveRets)/len(AlgoRetList)
print("Average returns of gains: ", statistics.mean(NumberofPositveRets))
print("Standard deviation of gains: ", statistics.stdev(NumberofPositveRets))
print("Averasge returns of losses: ", statistics.mean(NumberofNegativeRets))
print("Standard deviation of losses: ", statistics.stdev(NumberofNegativeRets))
print(PctofSuccess)

print("Sum of Algo Rets: ", sum(AlgoRetList))

plt.show()