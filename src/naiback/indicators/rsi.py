
from naiback.indicators.ema import EMA

def _calc_rsi(g, l):
    if g is None or l is None:
        return None
    if l == 0:
        return 100
    return 100 - 100 / (1 + g / l)

def RSI(data, period):
    diffs = [0]
    prevd = data[0]
    for d in data[1:]:
        diffs.append(d - prevd)
        prevd = d

    gains = EMA([max(x, 0) for x in diffs], period, 1. / period)
    losses = EMA([-min(x, 0) for x in diffs], period, 1. / period)
    return [_calc_rsi(g, l) for (g, l) in zip(gains, losses)]
