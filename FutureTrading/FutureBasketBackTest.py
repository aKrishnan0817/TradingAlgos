import pandas as pd
import numpy as np
# Read in data
# Gold
dfGold = pd.read_csv('gc1History.csv')
print(dfGold.head())
# Natural Gas
dfNatGas = pd.read_csv('ng1History.csv')
# Copper
dfCopper = pd.read_csv('hg1History.csv')
# Iron Ore
dfIron = pd.read_csv('ioe1History.csv')
# Wheat
dfWheat = pd.read_csv('w1History.csv')
# E-Mini
dfEmini = pd.read_csv('es1History.csv')
# Ten Year Bond
dfTY = pd.read_csv('ty1History.csv')
# Nasdaq 100
dfNQ = pd.read_csv('nq1History.csv')
# Russell 2000: Small cap stocks
dfRussell = pd.read_csv('rty1History.csv')
# Oil
dfOil = pd.read_csv('cl1History.csv')

# the idea is to hold this basket of divesified commodities and make changes as the indicators change

# Lets just try one future: es1
from FuncFuturesTrades import GetMovingAverageByIndex
from FuncFuturesTrades import FuturesMomentum
from FuncFuturesTrades import FuturesZValAlgo
from FuncFuturesTrades import FuturesPctChangeAlgo
from FuncFuturesTrades import FuturesMomChange

MADays = 10
# First position
CurrentPosition = -1

# assumption here is that the decision to go long or short is made at the close and that the
# closing price is available to make that determination

IndexReturnList = list()
CurrentPositionList = list()
ReturnList = list()
DateList = list()
print(dfEmini.loc[12,'Dates'])
StartIndex = MADays + 1
DateList = dfEmini['Dates'].to_list()
for i in range(0,StartIndex):
    ReturnList.append(0)
    CurrentPositionList.append(-1)

    IndexReturnList.append(-1)

print(ReturnList)

MAFast = 1
MASlow = 2
for i in range(StartIndex,len(dfEmini)):
    # Calculate the return for the day
    IndexReturn = (dfEmini.loc[i, 'PX_LAST'] - dfEmini.loc[i - 1, 'PX_LAST']) / dfEmini.loc[i-1, 'PX_LAST']
    if CurrentPosition == 1:
        Return = (dfEmini.loc[i,'PX_LAST'] - dfEmini.loc[i-1,'PX_LAST'])/dfEmini.loc[i-1,'PX_LAST']
    elif CurrentPosition == 0:
        Return = -(dfEmini.loc[i, 'PX_LAST'] - dfEmini.loc[i - 1, 'PX_LAST']) / dfEmini.loc[i-1, 'PX_LAST']
    elif CurrentPosition == -1:
        Return = 0

    ReturnList.append(Return)
    CurrentPositionList.append(CurrentPosition)
    IndexReturnList.append(IndexReturn)

    # Determine next day's position at today's close

    MADays = 10
    Threshold = 1.25
    Long = FuturesZValAlgo(dfEmini, i, MADays, Threshold)
    #Long = FuturesPctChangeAlgo(dfEmini, i, MADays)
    #Long = FuturesMomChange(dfEmini, i, MASlow, MAFast)

    #MADays = 2
    #Long = FuturesMomentum(dfEmini, i, MADays)

    if Long != CurrentPosition:
        CurrentPosition = Long

print("ES Total Return: ", sum(ReturnList))


DictOut = {'Dates': DateList,'Position':CurrentPositionList,'Returns': ReturnList,'IndexReturn':IndexReturnList}

dfOut = pd.DataFrame(DictOut)

dfOut.to_csv("EminiReturns.csv")

EminiReturns = ReturnList




# assumption here is that the decision to go long or short is made at the close and that the
# closing price is available to make that determination
# TY: Ten Year Bond Future
CurrentPosition = 1
IndexReturnList = list()
CurrentPositionList = list()
ReturnList = list()

StartIndex = MADays + 1

for i in range(0,StartIndex):
    ReturnList.append(0)
    CurrentPositionList.append(-1)

    IndexReturnList.append(-1)


for i in range(StartIndex,len(dfTY)):
    # Calculate the return for the day
    IndexReturn = (dfTY.loc[i, 'PX_LAST'] - dfTY.loc[i - 1, 'PX_LAST']) / dfTY.loc[i-1, 'PX_LAST']
    if CurrentPosition == 1:
        Return = (dfTY.loc[i,'PX_LAST'] - dfTY.loc[i-1,'PX_LAST'])/dfTY.loc[i-1,'PX_LAST']
    elif CurrentPosition == 0:
        Return = -(dfTY.loc[i, 'PX_LAST'] - dfTY.loc[i - 1, 'PX_LAST']) / dfTY.loc[i-1, 'PX_LAST']
    elif CurrentPosition == -1:
        Return = 0

    ReturnList.append(Return)
    CurrentPositionList.append(CurrentPosition)
    IndexReturnList.append(IndexReturn)

    # Determine next day's position at today's close
    #Long = FuturesMomentum(dfEmini, i, MADays)
    MADays = 10
    Threshold = 0.5
    Long = FuturesZValAlgo(dfTY, i, MADays, Threshold)
    #Long = FuturesPctChangeAlgo(dfTY, i, 1)
    #Long = FuturesMomChange(dfEmini, i, MASlow, MAFast)

    if Long != CurrentPosition:
        CurrentPosition = Long




DictOut = {'Dates': DateList,'Position':CurrentPositionList,'Returns': ReturnList,'IndexReturn':IndexReturnList}

dfOut = pd.DataFrame(DictOut)

dfOut.to_csv("TYReturns.csv")

TYReturns = ReturnList
print("TY Total return = ", sum(ReturnList))



# # CL: Oil
# MADays = 10
# CurrentPosition = 1
# IndexReturnList = list()
# CurrentPositionList = list()
# ReturnList = list()
#
# StartIndex = MADays + 1
#
# for i in range(0,StartIndex):
#     ReturnList.append(0)
#     CurrentPositionList.append(-1)
#
#     IndexReturnList.append(-1)
#
# for i in range(StartIndex,len(dfOil)):
#     # Calculate the return for the day
#     IndexReturn = (dfOil.loc[i, 'PX_LAST'] - dfOil.loc[i - 1, 'PX_LAST']) / dfOil.loc[i-1, 'PX_LAST']
#     if CurrentPosition == 1:
#         Return = (dfOil.loc[i,'PX_LAST'] - dfOil.loc[i-1,'PX_LAST'])/dfOil.loc[i-1,'PX_LAST']
#     elif CurrentPosition == 0:
#         Return = -(dfOil.loc[i, 'PX_LAST'] - dfOil.loc[i - 1, 'PX_LAST']) / dfOil.loc[i-1, 'PX_LAST']
#     elif CurrentPosition == -1:
#         Return = 0
#
#     ReturnList.append(Return)
#     CurrentPositionList.append(CurrentPosition)
#     IndexReturnList.append(IndexReturn)
#
#     # Determine next day's position at today's close
#     #Long = FuturesMomentum(dfEmini, i, MADays)
#     MADays = 2
#     Threshold = 1.25
#     Long = FuturesZValAlgo(dfOil, i, MADays, Threshold)
#     #Long = FuturesPctChangeAlgo(dfTY, i, 1)
#     #Long = FuturesMomChange(dfEmini, i, MASlow, MAFast)
#
#     if Long != CurrentPosition:
#         CurrentPosition = Long
#
#
#
#
# DictOut = {'Dates': DateList,'Position':CurrentPositionList,'Returns': ReturnList,'IndexReturn':IndexReturnList}
#
# dfOut = pd.DataFrame(DictOut)
#
# dfOut.to_csv("CLReturns.csv")
#
# OilReturns = ReturnList
# print("Oil Total return = ", sum(ReturnList))

# GC: Gold
MADays = 10
CurrentPosition = 1
IndexReturnList = list()
CurrentPositionList = list()
ReturnList = list()

StartIndex = MADays + 1

for i in range(0,StartIndex):
    ReturnList.append(0)
    CurrentPositionList.append(-1)

    IndexReturnList.append(-1)

for i in range(StartIndex,len(dfOil)):
    # Calculate the return for the day
    IndexReturn = (dfGold.loc[i, 'PX_LAST'] - dfGold.loc[i - 1, 'PX_LAST']) / dfGold.loc[i-1, 'PX_LAST']
    if CurrentPosition == 1:
        Return = (dfGold.loc[i,'PX_LAST'] - dfGold.loc[i-1,'PX_LAST'])/dfGold.loc[i-1,'PX_LAST']
    elif CurrentPosition == 0:
        Return = -(dfGold.loc[i, 'PX_LAST'] - dfGold.loc[i - 1, 'PX_LAST']) / dfGold.loc[i-1, 'PX_LAST']
    elif CurrentPosition == -1:
        Return = 0

    ReturnList.append(Return)
    CurrentPositionList.append(CurrentPosition)
    IndexReturnList.append(IndexReturn)

    # Determine next day's position at today's close
    #Long = FuturesMomentum(dfEmini, i, MADays)
    MADays = 10
    Threshold = 1.25
    Long = FuturesZValAlgo(dfGold, i, MADays, Threshold)
    #Long = FuturesPctChangeAlgo(dfTY, i, 1)
    #Long = FuturesMomChange(dfEmini, i, MASlow, MAFast)

    if Long != CurrentPosition:
        CurrentPosition = Long




DictOut = {'Dates': DateList,'Position':CurrentPositionList,'Returns': ReturnList,'IndexReturn':IndexReturnList}

dfOut = pd.DataFrame(DictOut)

dfOut.to_csv("GoldReturns.csv")

GoldReturns = ReturnList
print("Gold Total return = ", sum(ReturnList))

# Russell: Small cap
MADays = 10
CurrentPosition = 1
IndexReturnList = list()
CurrentPositionList = list()
ReturnList = list()

StartIndex = 4312+MADays

for i in range(0,StartIndex):
    ReturnList.append(0)
    CurrentPositionList.append(-1)

    IndexReturnList.append(-1)

for i in range(StartIndex,len(dfOil)):
    # Calculate the return for the day
    IndexReturn = (dfRussell.loc[i, 'PX_LAST'] - dfRussell.loc[i - 1, 'PX_LAST']) / dfRussell.loc[i-1, 'PX_LAST']
    if CurrentPosition == 1:
        Return = (dfRussell.loc[i,'PX_LAST'] - dfRussell.loc[i-1,'PX_LAST'])/dfRussell.loc[i-1,'PX_LAST']
    elif CurrentPosition == 0:
        Return = -(dfRussell.loc[i, 'PX_LAST'] - dfRussell.loc[i - 1, 'PX_LAST']) / dfRussell.loc[i-1, 'PX_LAST']
    elif CurrentPosition == -1:
        Return = 0

    ReturnList.append(Return)
    CurrentPositionList.append(CurrentPosition)
    IndexReturnList.append(IndexReturn)

    # Determine next day's position at today's close
    #Long = FuturesMomentum(dfEmini, i, MADays)
    MADays = 10
    Threshold = 1.25
    Long = FuturesZValAlgo(dfRussell, i, MADays, Threshold)
    #Long = FuturesPctChangeAlgo(dfTY, i, 1)
    #Long = FuturesMomChange(dfEmini, i, MASlow, MAFast)

    if Long != CurrentPosition:
        CurrentPosition = Long




DictOut = {'Dates': DateList,'Position':CurrentPositionList,'Returns': ReturnList,'IndexReturn':IndexReturnList}

dfOut = pd.DataFrame(DictOut)

dfOut.to_csv("RussellReturns.csv")

RussellReturns = ReturnList
print("Russell Total return = ", sum(ReturnList))

# Nasdaq: NQ
MADays = 10
CurrentPosition = 1
IndexReturnList = list()
CurrentPositionList = list()
ReturnList = list()

StartIndex = MADays + 1

for i in range(0,StartIndex):
    ReturnList.append(0)
    CurrentPositionList.append(-1)

    IndexReturnList.append(-1)

for i in range(StartIndex,len(dfOil)):
    # Calculate the return for the day
    IndexReturn = (dfNQ.loc[i, 'PX_LAST'] - dfNQ.loc[i - 1, 'PX_LAST']) / dfNQ.loc[i-1, 'PX_LAST']
    if CurrentPosition == 1:
        Return = (dfNQ.loc[i,'PX_LAST'] - dfNQ.loc[i-1,'PX_LAST'])/dfNQ.loc[i-1,'PX_LAST']
    elif CurrentPosition == 0:
        Return = -(dfNQ.loc[i, 'PX_LAST'] - dfNQ.loc[i - 1, 'PX_LAST']) / dfNQ.loc[i-1, 'PX_LAST']
    elif CurrentPosition == -1:
        Return = 0

    ReturnList.append(Return)
    CurrentPositionList.append(CurrentPosition)
    IndexReturnList.append(IndexReturn)

    # Determine next day's position at today's close
    #Long = FuturesMomentum(dfEmini, i, MADays)
    MADays = 10
    Threshold = 1
    Long = FuturesZValAlgo(dfNQ, i, MADays, Threshold)
    #Long = FuturesPctChangeAlgo(dfTY, i, 1)
    #Long = FuturesMomChange(dfEmini, i, MASlow, MAFast)

    #MADays = 1
    #Long = FuturesMomentum(dfEmini, i, MADays)

    if Long != CurrentPosition:
        CurrentPosition = Long




DictOut = {'Dates': DateList,'Position':CurrentPositionList,'Returns': ReturnList,'IndexReturn':IndexReturnList}

dfOut = pd.DataFrame(DictOut)

dfOut.to_csv("NQReturns.csv")

NQReturns = ReturnList
print("NQ Total return = ", sum(ReturnList))

# Natural Gas: NG
MADays = 10
CurrentPosition = 1
IndexReturnList = list()
CurrentPositionList = list()
ReturnList = list()

StartIndex = MADays + 1

for i in range(0,StartIndex):
    ReturnList.append(0)
    CurrentPositionList.append(-1)

    IndexReturnList.append(-1)

for i in range(StartIndex,len(dfOil)):
    # Calculate the return for the day
    IndexReturn = (dfNatGas.loc[i, 'PX_LAST'] - dfNatGas.loc[i - 1, 'PX_LAST']) / dfNatGas.loc[i-1, 'PX_LAST']
    if CurrentPosition == 1:
        Return = (dfNatGas.loc[i,'PX_LAST'] - dfNatGas.loc[i-1,'PX_LAST'])/dfNatGas.loc[i-1,'PX_LAST']
    elif CurrentPosition == 0:
        Return = -(dfNatGas.loc[i, 'PX_LAST'] - dfNatGas.loc[i - 1, 'PX_LAST']) / dfNatGas.loc[i-1, 'PX_LAST']
    elif CurrentPosition == -1:
        Return = 0

    ReturnList.append(Return)
    CurrentPositionList.append(CurrentPosition)
    IndexReturnList.append(IndexReturn)

    # Determine next day's position at today's close
    #Long = FuturesMomentum(dfEmini, i, MADays)
    MADays = 10
    Threshold = 1
    Long = FuturesZValAlgo(dfNatGas, i, MADays, Threshold)
    #Long = FuturesPctChangeAlgo(dfTY, i, 1)
    #Long = FuturesMomChange(dfEmini, i, MASlow, MAFast)

    if Long != CurrentPosition:
        CurrentPosition = Long




DictOut = {'Dates': DateList,'Position':CurrentPositionList,'Returns': ReturnList,'IndexReturn':IndexReturnList}

dfOut = pd.DataFrame(DictOut)

dfOut.to_csv("NatGasReturns.csv")

NatGasReturns = ReturnList
print("NatGas Total return = ", sum(ReturnList))

# Copper
MADays = 10
CurrentPosition = 1
IndexReturnList = list()
CurrentPositionList = list()
ReturnList = list()

StartIndex = MADays + 1

for i in range(0,StartIndex):
    ReturnList.append(0)
    CurrentPositionList.append(-1)

    IndexReturnList.append(-1)

for i in range(StartIndex,len(dfCopper)):
    # Calculate the return for the day
    IndexReturn = (dfCopper.loc[i, 'PX_LAST'] - dfCopper.loc[i - 1, 'PX_LAST']) / dfCopper.loc[i-1, 'PX_LAST']
    if CurrentPosition == 1:
        Return = (dfCopper.loc[i,'PX_LAST'] - dfCopper.loc[i-1,'PX_LAST'])/dfCopper.loc[i-1,'PX_LAST']
    elif CurrentPosition == 0:
        Return = -(dfCopper.loc[i, 'PX_LAST'] - dfCopper.loc[i - 1, 'PX_LAST']) / dfCopper.loc[i-1, 'PX_LAST']
    elif CurrentPosition == -1:
        Return = 0

    ReturnList.append(Return)
    CurrentPositionList.append(CurrentPosition)
    IndexReturnList.append(IndexReturn)

    # Determine next day's position at today's close
    #Long = FuturesMomentum(dfEmini, i, MADays)
    MADays = 10
    Threshold = 1
    Long = FuturesZValAlgo(dfCopper, i, MADays, Threshold)
    #Long = FuturesPctChangeAlgo(dfTY, i, 1)
    #Long = FuturesMomChange(dfEmini, i, MASlow, MAFast)

    if Long != CurrentPosition:
        CurrentPosition = Long




DictOut = {'Dates': DateList,'Position':CurrentPositionList,'Returns': ReturnList,'IndexReturn':IndexReturnList}

dfOut = pd.DataFrame(DictOut)

dfOut.to_csv("CopperReturns.csv")

CopperReturns = ReturnList
print("Copper Total return = ", sum(ReturnList))

# Wheat
MADays = 10
CurrentPosition = 1
IndexReturnList = list()
CurrentPositionList = list()
ReturnList = list()

StartIndex = MADays + 1

for i in range(0,StartIndex):
    ReturnList.append(0)
    CurrentPositionList.append(-1)

    IndexReturnList.append(-1)

for i in range(StartIndex,len(dfWheat)):
    # Calculate the return for the day
    IndexReturn = (dfWheat.loc[i, 'PX_LAST'] - dfWheat.loc[i - 1, 'PX_LAST']) / dfWheat.loc[i-1, 'PX_LAST']
    if CurrentPosition == 1:
        Return = (dfWheat.loc[i,'PX_LAST'] - dfWheat.loc[i-1,'PX_LAST'])/dfWheat.loc[i-1,'PX_LAST']
    elif CurrentPosition == 0:
        Return = -(dfWheat.loc[i, 'PX_LAST'] - dfWheat.loc[i - 1, 'PX_LAST']) / dfWheat.loc[i-1, 'PX_LAST']
    elif CurrentPosition == -1:
        Return = 0

    ReturnList.append(Return)
    CurrentPositionList.append(CurrentPosition)
    IndexReturnList.append(IndexReturn)

    # Determine next day's position at today's close
    #Long = FuturesMomentum(dfEmini, i, MADays)
    MADays = 30
    Threshold = 1.25
    Long = FuturesZValAlgo(dfWheat, i, MADays, Threshold)
    #Long = FuturesPctChangeAlgo(dfTY, i, 1)
    #Long = FuturesMomChange(dfEmini, i, MASlow, MAFast)

    if Long != CurrentPosition:
        CurrentPosition = Long




DictOut = {'Dates': DateList,'Position':CurrentPositionList,'Returns': ReturnList,'IndexReturn':IndexReturnList}

dfOut = pd.DataFrame(DictOut)

dfOut.to_csv("WheatReturns.csv")

WheatReturns = ReturnList
print("Wheat Total return = ", sum(ReturnList))

# # Iron
# MADays = 10
# CurrentPosition = 1
# IndexReturnList = list()
# CurrentPositionList = list()
# ReturnList = list()
#
# StartIndex = MADays + 1
# StartIndex = 3341 + MADays + 1
#
# for i in range(0,StartIndex):
#     ReturnList.append(0)
#     CurrentPositionList.append(-1)
#
#     IndexReturnList.append(-1)
#
# for i in range(StartIndex,len(dfIron)):
#     # Calculate the return for the day
#     IndexReturn = (dfIron.loc[i, 'PX_LAST'] - dfIron.loc[i - 1, 'PX_LAST']) / dfIron.loc[i-1, 'PX_LAST']
#     if CurrentPosition == 1:
#         Return = (dfIron.loc[i,'PX_LAST'] - dfIron.loc[i-1,'PX_LAST'])/dfIron.loc[i-1,'PX_LAST']
#     elif CurrentPosition == 0:
#         Return = -(dfIron.loc[i, 'PX_LAST'] - dfIron.loc[i - 1, 'PX_LAST']) / dfIron.loc[i-1, 'PX_LAST']
#     elif CurrentPosition == -1:
#         Return = 0
#
#     ReturnList.append(Return)
#     CurrentPositionList.append(CurrentPosition)
#     IndexReturnList.append(IndexReturn)
#
#     # Determine next day's position at today's close
#     #Long = FuturesMomentum(dfEmini, i, MADays)
#     MADays = 10
#     Threshold = 1.25
#     Long = FuturesZValAlgo(dfIron, i, MADays, Threshold)
#     #Long = FuturesPctChangeAlgo(dfTY, i, 1)
#     #Long = FuturesMomChange(dfEmini, i, MASlow, MAFast)
#
#     if Long != CurrentPosition:
#         CurrentPosition = Long
#
#
#
#
# DictOut = {'Dates': DateList,'Position':CurrentPositionList,'Returns': ReturnList,'IndexReturn':IndexReturnList}
#
# dfOut = pd.DataFrame(DictOut)
#
# dfOut.to_csv("IronReturns.csv")
#
# IronReturns = ReturnList
# print("Iron Total return = ", sum(ReturnList))







Factor = 1
FactorNatGas = 0.1 # Lots of vol and risk
FactorCopper = 1
FactorWheat = 1
FactorIron = 1
TotalReturn = Factor*np.array(EminiReturns) + Factor * np.array(TYReturns) + Factor * np.array(GoldReturns) +  \
              Factor * np.array(RussellReturns) + Factor * np.array(NQReturns) + FactorNatGas * np.array(NatGasReturns) \
              + FactorCopper * np.array(CopperReturns) + FactorWheat * np.array(WheatReturns)


print("Total Return = ", sum(TotalReturn))






