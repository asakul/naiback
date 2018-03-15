
class Position:

    def __init__(self, ticker):
        self.ticker = ticker
        self.entry_price = None
        self.entry_metadata = {}
        self.exit_price = None
        self.exit_metadata = {}
        self.size = None
        self.total_pnl = 0

    def entry_commission(self):
        return self.entry_metadata['commission']

    def entry_bar(self):
        return self.entry_metadata['bar']

    def pnl(self):
        return self.total_pnl

    def enter(self, price, amount, **kwargs):
        self.entry_price = price
        self.size = amount

        for k, v in kwargs.items():
            self.entry_metadata[k] = v

    def exit(self, price):
        self.exit_price = price
        self.total_pnl += (self.exit_price - self.entry_price) * self.size
        self.size = 0


