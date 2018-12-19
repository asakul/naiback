
import numpy as np

def SMA(data, period):
    result = np.zeros(len(data))
    for i in range(1, len(data)):
        result[i] = sum(data[max(0, i-period+1):(i + 1)]) / period
    return result

