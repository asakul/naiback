
from .analyzer import Analyzer

from prettytable import PrettyTable

def render_float(a):
    return "{:.3f}".format(a)


def render_ratio(a, b):
    if b != 0:
        return a / b
    else:
        return "∞"

class StatsAnalyzer(Analyzer):

    def __init__(self, strategy):
        self.strategy = strategy

    def generate_plain_text(self):
        positions = self.strategy.broker.retired_positions() # TODO also add open positions
        stats = self.calc_stats(positions)

        table = PrettyTable()
        table.field_names = ["", "All positions", "Long only", "Short only"]
        table.add_row(["Net profit", render_float(stats['all']['net_profit']), render_float(stats['long']['net_profit']), render_float(stats['short']['net_profit'])])
        table.add_row(["Bars in trade", stats['all']['bars_in_trade'], stats['long']['bars_in_trade'], stats['short']['bars_in_trade']])
        table.add_row(["Profit per bar", render_float(stats['all']['profit_per_bar']), render_float(stats['long']['profit_per_bar']), render_float(stats['short']['profit_per_bar'])])
        table.add_row(["Number of trades", stats['all']['number_of_trades'], stats['long']['number_of_trades'], stats['short']['number_of_trades']])
        table.add_row(["Avg. profit", render_float(stats['all']['avg']), render_float(stats['long']['avg']), render_float(stats['short']['avg'])])
        table.add_row(["Avg. profit, %", render_float(stats['all']['avg_percentage']), render_float(stats['long']['avg_percentage']), render_float(stats['short']['avg_percentage'])])
        table.add_row(["Avg. bars in trade", render_float(stats['all']['avg_bars']), render_float(stats['long']['avg_bars']), render_float(stats['short']['avg_bars'])])
        table.add_row(["Winning trades", stats['all']['won'], stats['long']['won'], stats['short']['won']])
        table.add_row(["Gross profit", render_float(stats['all']['total_won']), render_float(stats['long']['total_won']), render_float(stats['short']['total_won'])])
        table.add_row(["Losing trades", stats['all']['lost'], stats['long']['lost'], stats['short']['lost']])
        table.add_row(["Gross loss", render_float(stats['all']['total_lost']), render_float(stats['long']['total_lost']), render_float(stats['short']['total_lost'])])
        table.add_row(["Profit factor", render_float(stats['all']['profit_factor']), render_float(stats['long']['profit_factor']), render_float(stats['short']['profit_factor'])])

        return table.get_string()

    def get_result(self):
        positions = self.strategy.broker.retired_positions() # TODO also add open positions
        stats = self.calc_stats(positions)
        return stats

    def calc_stats(self, positions):
        longs = list(filter(lambda x: x.is_long(), positions))
        shorts = list(filter(lambda x: x.is_short(), positions))

        result = { 'all' : {}, 'long' : {}, 'short' : {} }

        result['all']['net_profit'] = sum([pos.pnl() for pos in positions])
        result['long']['net_profit'] = sum([pos.pnl() for pos in longs])
        result['short']['net_profit'] = sum([pos.pnl() for pos in shorts])

        result['all']['bars_in_trade'] = sum([pos.bars_in_trade() for pos in positions])
        result['long']['bars_in_trade'] = sum([pos.bars_in_trade() for pos in longs])
        result['short']['bars_in_trade'] = sum([pos.bars_in_trade() for pos in shorts])

        result['all']['profit_per_bar'] = render_ratio(result['all']['net_profit'], result['all']['bars_in_trade'])
        result['long']['profit_per_bar'] = render_ratio(result['long']['net_profit'], result['long']['bars_in_trade'])
        result['short']['profit_per_bar'] = render_ratio(result['short']['net_profit'], result['short']['bars_in_trade'])

        result['all']['number_of_trades'] = len(positions)
        result['long']['number_of_trades'] = len(list(longs))
        result['short']['number_of_trades'] = len(list(shorts))

        result['all']['avg'] = render_ratio(result['all']['net_profit'], result['all']['number_of_trades'])
        result['long']['avg'] = render_ratio(result['long']['net_profit'], result['long']['number_of_trades'])
        result['short']['avg'] = render_ratio(result['short']['net_profit'], result['short']['number_of_trades'])

        result['all']['avg_percentage'] = render_ratio(sum([pos.profit_percentage() for pos in positions]), result['all']['number_of_trades'])
        result['long']['avg_percentage'] = render_ratio(sum([pos.profit_percentage() for pos in longs]), result['long']['number_of_trades'])
        result['short']['avg_percentage'] = render_ratio(sum([pos.profit_percentage() for pos in shorts]), result['short']['number_of_trades'])

        result['all']['avg_bars'] = render_ratio(result['all']['bars_in_trade'], result['all']['number_of_trades'])
        result['long']['avg_bars'] = render_ratio(result['long']['bars_in_trade'], result['long']['number_of_trades'])
        result['short']['avg_bars'] = render_ratio(result['short']['bars_in_trade'], result['short']['number_of_trades'])

        result['all']['won'] = len(list(filter(lambda pos: pos.pnl() > 0, positions)))
        result['long']['won'] = len(list(filter(lambda pos: pos.pnl() > 0, longs)))
        result['short']['won'] = len(list(filter(lambda pos: pos.pnl() > 0, shorts)))

        result['all']['lost'] = len(list(filter(lambda pos: pos.pnl() <= 0, positions)))
        result['long']['lost'] = len(list(filter(lambda pos: pos.pnl() <= 0, longs)))
        result['short']['lost'] = len(list(filter(lambda pos: pos.pnl() <= 0, shorts)))

        result['all']['total_won'] = sum(map(lambda pos: pos.pnl(), filter(lambda pos: pos.pnl() > 0, positions)))
        result['long']['total_won'] = sum(map(lambda pos: pos.pnl(), filter(lambda pos: pos.pnl() > 0, longs)))
        result['short']['total_won'] = sum(map(lambda pos: pos.pnl(), filter(lambda pos: pos.pnl() > 0, shorts)))

        result['all']['total_lost'] = sum(map(lambda pos: pos.pnl(), filter(lambda pos: pos.pnl() <= 0, positions)))
        result['long']['total_lost'] = sum(map(lambda pos: pos.pnl(), filter(lambda pos: pos.pnl() <= 0, longs)))
        result['short']['total_lost'] = sum(map(lambda pos: pos.pnl(), filter(lambda pos: pos.pnl() <= 0, shorts)))

        result['all']['profit_factor'] = render_ratio(result['all']['total_won'], -result['all']['total_lost'])
        result['long']['profit_factor'] = render_ratio(result['long']['total_won'], -result['long']['total_lost'])
        result['short']['profit_factor'] = render_ratio(result['short']['total_won'], -result['short']['total_lost'])

        return result
