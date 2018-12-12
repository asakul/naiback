
import numpy as np

def Highest(data, period):
    result = np.zeros(len(data))
    if len(result) == 0:
        return result
    result[0] = data[0]
    for i in range(1, len(data)):
        result[i] = max(data[max(0, i - period):(i+1)])

    return result
    
def HighestValue(data, index, period):
    if len(data) == 0 or index >= len(data):
        return None
    if index == 0:
        return data[0]
    return max(data[max(0, index - period):(index+1)])
