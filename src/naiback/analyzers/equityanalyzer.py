
from .analyzer import Analyzer

import numpy as np

class EquityAnalyzer(Analyzer):

    def __init__(self, strategy):
        self.strategy = strategy
        self.bar_to_pos = []

    def get_result(self):
        positions = self.strategy.broker.retired_positions() # TODO also add open positions
        bars = self.strategy.all_bars
        equity = self.calc_equity(positions, bars[0])
        return equity

    def calc_equity(self, positions, bars):
        close = bars.close

        cumulative_pnl = 0

        equity = []

        prev_p = 0
        self.calculate_lookup_table(positions, len(close))
        for (bar_num, p) in enumerate(close):
            active_positions = self.positions_for_bar(positions, bar_num)
            for pos in active_positions:
                if pos.entry_bar() == bar_num:
                    if pos.is_long():
                        cumulative_pnl += (p - pos.entry_price())
                    else:
                        cumulative_pnl -= (p - pos.entry_price())
                elif pos.exit_bar() == bar_num:
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
                    
    def positions_for_bar(self, positions, bar_num):
        result = []
        for pos_index in self.bar_to_pos[bar_num]:
            pos = positions[pos_index]
            result.append(pos)
        return result

    def calculate_lookup_table(self, positions, length):
        self.bar_to_pos = []
        for i in range(0, length):
            self.bar_to_pos.append([])
        for pos_index, pos in enumerate(positions):
            for i in range(pos.entry_bar(), pos.exit_bar() + 1):
                self.bar_to_pos[i].append(pos_index)
