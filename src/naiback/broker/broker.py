
class Broker:
    """
    Broker has several responsibilities (so called SRP, or several responsibilities principle):
    1) Track money amount on trading account
    2) Track active positions
    3) Subtract commissions/slippage
    4) Validate issued orders and reject them if needed
    """

    def __init__(self, initial_cash=100000.):
        self.cash = initial_cash
        self.positions = []

