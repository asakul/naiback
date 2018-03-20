
def _update(v, d, alpha):
    return v * (1 - alpha) + d * alpha

def EMA(data, period, alpha=None):
    if alpha is None:
        alpha = 2. / (period + 1)
    result = []
    v = None
    for d in data:
        if d is None:
            result.append(None)
        elif v is None:
            result.append(None)
            v = d
        else:
            v = _update(v, d, alpha)
            result.append(v)
    return result


