
import numpy as np

def SMMA(values, period):
    smma = np.zeros(len(values))
    alpha = (period - 1) / period

    smma[0] = values[0]
    for i in range(1, len(values)):
        smma[i] = smma[i - 1] * alpha + values[i] * (1 - alpha)

    return smma
    
