
import pytest
import datetime

from naiback.broker.broker import Broker

def test_broker_cash():
    broker = Broker(initial_cash=100000.)

    assert broker.cash() == 100000.

def test_broker_add_position_enough_cash():
    broker = Broker(initial_cash=100)

    pos = broker.add_position('FOO', price=10, amount=1, bar_index=0)

    assert pos.entry_price() == 10
    assert pos.size() == 1

def test_broker_add_position_not_enough_cash():
    broker = Broker(initial_cash=100)

    pos = broker.add_position('FOO', price=1000, amount=1, bar_index=0)

    assert pos is None

def test_broker_percentage_commissions():
    broker = Broker(initial_cash=100)
    broker.set_commission(percentage=0.05) # 0.05%

    pos = broker.add_position('FOO', price=10, amount=1, bar_index=0)

    should_be_cash = 100 - 10 - 10 * 0.01 * 0.05

    assert (broker.cash() - should_be_cash) < 0.00001

def test_broker_all_position():
    broker = Broker(initial_cash=100)

    pos = broker.add_position('FOO', price=10, amount=1, bar_index=0)

    assert pos in broker.all_positions()

def test_broker_close_position():
    broker = Broker(initial_cash=100)

    pos = broker.add_position('FOO', price=10, amount=1, bar_index=0)
    broker.close_position(pos, price=12, bar_index=1)

    assert broker.cash() == 100 + 2

def test_broker_close_position_with_commission():
    broker = Broker(initial_cash=100)
    
    broker.set_commission(percentage=1) # 1%

    pos = broker.add_position('FOO', price=10, amount=1, bar_index=0)
    broker.close_position(pos, price=12, bar_index=1)

    assert broker.cash() == 100 + 2 - (10 + 12) * 0.01

