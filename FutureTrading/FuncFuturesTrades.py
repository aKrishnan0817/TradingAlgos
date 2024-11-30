import numpy as np
def GetMovingAverage(dfFut, Days):

    LastPrice = dfFut['PX_LAST'].to_list()
    MA = list()
    for i in range(Days,len(LastPrice)):
        a = LastPrice[i-Days:i]
        MA[i] = sum(a)/len(a)

    return MA


def GetMovingAverageByIndex(dfFut, Days, Index):
    PriorIndex = Index # decision made at close
    LastPrice = dfFut.loc[PriorIndex-Days:PriorIndex,'PX_LAST'].to_list()
    MA = sum(LastPrice)/len(LastPrice)

    return MA

def GetZValueByIndex(dfFut, Days, Index):
    PriorIndex = Index
    LastPrice = dfFut.loc[PriorIndex - Days:PriorIndex, 'PX_LAST'].to_list()
    stdev = np.std(LastPrice)
    avg = np.average(LastPrice)

    zval = (dfFut.loc[Index,'PX_LAST']-avg)/stdev


    return zval

def GetPctChangeByIndex(dfFut, Days, Index):
    PriorIndex = Index
    LastPrice = dfFut.loc[PriorIndex - Days:PriorIndex, 'PX_LAST'].to_list()
    PctChange = (LastPrice[-1]-LastPrice[0])/LastPrice[0]

    return PctChange

def FuturesZValAlgo(dfFut, index, MADays, Threshold):
    Zval = GetZValueByIndex(dfFut, MADays, index)
    Long = -1
    if Zval > Threshold:
        Long = 0
    elif Zval < -Threshold:
        Long = 1

    return Long

def FuturesPctChangeAlgo(dfFut, index, Days):
    PctChange = GetPctChangeByIndex(dfFut, Days, index)
    Long = -1
    Delta = 0.0
    if PctChange >= Delta:
        Long = 0
    elif PctChange < -Delta:
        Long = 1

    return Long





def FuturesMomentum(dfFut, index, MADays):
    # Lets calculate MA (Moving average)
    # If price > MA, then stay long else go short

    MA = GetMovingAverageByIndex(dfFut, MADays, index)

    if dfFut.loc[index,'PX_LAST'] > MA:
        Long = 0
    else:
        Long = 1

    return Long

def FuturesMomChange(dfFut, index, MASlow, MAFast):
    MASlow = GetMovingAverageByIndex(dfFut, MASlow, index)
    MAFast = GetMovingAverageByIndex(dfFut, MAFast, index)

    Long = -1
    if MAFast > MASlow:
        Long = 1
    else:
        Long = 0

    return Long
