
from naiback.broker.position import Position

class Broker:
    """
    Broker has several responsibilities (so called SRP, or several responsibilities principle):
    1) Track money amount on trading account
    2) Track active positions
    3) Subtract commissions/slippage
    4) Validate issued orders and reject them if needed
    """

    def __init__(self, initial_cash=100000.):
        self.cash_ = initial_cash
        self.positions = []
        self.retired_positions_ = []
        self.commission_percentage = 0
        self.timestamp = None

    def cash(self):
        return self.cash_

    def set_timestamp(self, ts):
        self.timestamp = ts

    def add_position(self, ticker, price, amount, bar_index):
        volume = abs(price * amount)
        #if amount > 0:
        #    if volume * (1 + 0.01 * self.commission_percentage) > self.cash_:
        #        return None
        pos = Position(ticker)
        pos.enter(price, amount, bar=bar_index, timestamp=self.timestamp)
        self.cash_ -= price * amount
        self.cash_ -= volume * 0.01 * self.commission_percentage
        self.positions.append(pos)
        return pos

    def close_position(self, pos, price, bar_index):
        volume = abs(price * pos.size())
        size = pos.size()
        pos.exit(price, bar=bar_index, timestamp=self.timestamp)

        self.retired_positions_.append(pos)
        self.positions.remove(pos)

        self.cash_ += price * size
        self.cash_ -= volume * 0.01 * self.commission_percentage
        return True

    def set_commission(self, percentage):
        self.commission_percentage = percentage

    def last_position(self):
        return self.positions[-1]

    def all_positions(self):
        return self.positions[:]

    def retired_positions(self):
        return self.retired_positions_

    def last_position_is_active(self):
        if len(self.positions) == 0:
            return False

        if self.last_position().exit_price() is None:
            return True

        return False

