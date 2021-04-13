
class Position:

    def __init__(self, ticker):
        self.ticker = ticker
        self.entry_price_ = None
        self.entry_metadata = {}
        self.exit_price_ = None
        self.exit_metadata = {}
        self.size_ = None
        self.original_size_ = None
        self.total_pnl = 0

    def entry_price(self):
        return self.entry_price_

    def exit_price(self):
        return self.exit_price_

    def size(self):
        return self.size_

    def original_size(self):
        return self.original_size_

    def is_long(self):
        return self.original_size_ > 0

    def is_short(self):
        return self.original_size_ < 0

    def entry_commission(self):
        try:
            return self.entry_metadata['commission']
        except KeyError:
            return 0

    def entry_bar(self):
        return self.entry_metadata['bar']

    def entry_time(self):
        return self.entry_metadata['timestamp']

    def exit_bar(self):
        return self.exit_metadata['bar']

    def exit_time(self):
        return self.exit_metadata['timestamp']

    def exit_commission(self):
        try:
            return self.exit_metadata['commission']
        except KeyError:
            return 0

    def bars_in_trade(self):
        return self.exit_bar() - self.entry_bar()

    def total_commission(self):
        commission = 0
        try:
            commission += self.entry_commission()
        except KeyError:
            pass
        try:
            commission += self.exit_commission()
        except KeyError:
            pass
        return commission

    def pnl(self):
        return self.total_pnl - self.total_commission()

    def profit_percentage(self):
        if self.is_long():
            return (self.exit_price() / self.entry_price() - 1 - (self.total_commission()) / self.entry_price()) * 100.
        else:
            return (1 - self.exit_price() / self.entry_price() - (self.total_commission()) / self.entry_price()) * 100.

    def enter(self, price, amount, **kwargs):
        self.entry_price_ = price
        self.size_ = amount
        self.original_size_ = amount

        for k, v in kwargs.items():
            self.entry_metadata[k] = v

    def exit(self, price, **kwargs):
        self.exit_price_ = price
        self.total_pnl += (self.exit_price() - self.entry_price()) * self.size() - self.total_commission()
        self.size_ = 0

        for k, v in kwargs.items():
            self.exit_metadata[k] = v


