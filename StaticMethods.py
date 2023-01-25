import numpy as np
import datetime


def getMinimum(input_double):
    res = input_double[0]
    for i in input_double:
        if res > i:
            res = i
    return res


def getMaximum(input_double):
    res = input_double[0]
    for i in input_double:
        if res < i:
            res = i
    return res


# enter amount_of_period  percent of filtered data
# 1                       68
# 2                       95
# 3                       99.7

def predictionLimits(data, amount_of_period=1):
    res = []
    mean_val = np.mean(data)
    st_dev = np.std(data)
    if amount_of_period < 1:
        amount_of_period = 1
    res.append(mean_val - amount_of_period * st_dev)
    res.append((mean_val + amount_of_period * st_dev))
    return res


def convertSecondsToTime(s):
    hours = s//3600
    minutes = (s-hours*3600)//60
    seconds = s-hours*3600-minutes*60
    milis = s-hours*3600-minutes*60-seconds
    return "Current time: "+str(hours)+"h. "+str(minutes)+"m. "+str(seconds)+"s. "+str(milis)+"ms"
