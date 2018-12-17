
from .analyzer import Analyzer

import numpy as np

class EquityAnalyzer(Analyzer):

    def __init__(self, strategy):
        self.strategy = strategy

    def get_result(self):
        positions = self.strategy.broker.retired_positions() # TODO also add open positions
        bars = self.strategy.all_bars
        equity = self.calc_equity(positions, bars[0])
        return equity

    def calc_equity(self, positions, bars):
        timestamp = bars.timestamp
        close = bars.close

        cumulative_pnl = 0

        equity = []

        prev_p = 0
        print(len(close), len(timestamp))
        for (p,ts) in zip(close, timestamp):
            active_positions = self.positions_for_timestamp(positions, ts)
            for pos in active_positions:
                if pos.entry_time() == ts:
                    if pos.is_long():
                        cumulative_pnl += (p - pos.entry_price())
                    else:
                        cumulative_pnl -= (p - pos.entry_price())
                elif pos.exit_time() == ts:
                    if pos.is_long():
                        cumulative_pnl += (pos.exit_price() - prev_p)
                    else:
                        cumulative_pnl -= (pos.exit_price() - prev_p)
                else:
                    if pos.is_long():
                        cumulative_pnl += (p - prev_p)
                    else:
                        cumulative_pnl -= (p - prev_p)
            equity.append(cumulative_pnl)

            prev_p = p
        return equity
                    
    def positions_for_timestamp(self, positions, timestamp):
        result = []
        for p in positions:
            if p.entry_time() <= timestamp and p.exit_time() >= timestamp:
                result.append(p)
        return result

        

