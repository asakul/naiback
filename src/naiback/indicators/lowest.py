
import numpy as np

def Lowest(data, period):
    result = np.zeros(len(data))
    if len(result) == 0:
        return result
    result[0] = data[0]
    for i in range(1, len(data)):
        result[i] = min(data[max(0, i - period + 1):(i+1)])

    return result
    
def LowestValue(data, index, period):
    if len(data) == 0 or index >= len(data):
        return None
    if index == 0:
        return data[0]
    return min(data[max(0, index - period + 1):(index+1)])
