
class Position:

    def __init__(self, ticker):
        self.ticker = ticker
        self.entry_price_ = None
        self.entry_metadata = {}
        self.exit_price_ = None
        self.exit_metadata = {}
        self.size_ = None
        self.total_pnl = 0

    def entry_price(self):
        return self.entry_price_

    def exit_price(self):
        return self.exit_price_

    def size(self):
        return self.size_

    def is_long(self):
        return self.size_ > 0

    def entry_commission(self):
        return self.entry_metadata['commission']

    def entry_bar(self):
        return self.entry_metadata['bar']

    def pnl(self):
        return self.total_pnl

    def enter(self, price, amount, **kwargs):
        self.entry_price_ = price
        self.size_ = amount

        for k, v in kwargs.items():
            self.entry_metadata[k] = v

    def exit(self, price, **kwargs):
        self.exit_price_ = price
        self.total_pnl += (self.exit_price() - self.entry_price()) * self.size()
        self.size_ = 0

        for k, v in kwargs.items():
            self.exit_metadata[k] = v


