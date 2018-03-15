
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
        self.commission_percentage = 0

    def cash(self):
        return self.cash_

    def add_position(self, ticker, price, amount):
        volume = abs(price * amount)
        if amount > 0:
            if volume * (1 + self.commission_percentage) > self.cash_:
                return None
        pos = Position(ticker)
        pos.enter(price, amount)
        self.cash_ -= (volume + volume * self.commission_percentage)
        self.positions.append(pos)
        return pos

    def set_commission(self, percentage):
        self.commission_percentage = percentage

    def all_positions(self):
        return self.positions

