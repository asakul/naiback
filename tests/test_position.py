
import pytest
import datetime

from naiback.broker.position import Position

@pytest.fixture
def position():
    return Position('FOO')

def test_position_enter(position):
    position.enter(3.50, 10)

    assert position.entry_price == 3.50
    assert position.size == 10

def test_position_enter_metadata(position):
    position.enter(3.50, 10, commission=0.1, bar=42)

    assert position.entry_metadata['commission'] == 0.1
    assert position.entry_metadata['bar'] == 42

def test_position_metadata_helpers(position):
    position.enter(3.50, 10, commission=0.1, bar=42)

    assert position.entry_commission() == 0.1
    assert position.entry_bar() == 42

def test_position_exit(position):
    position.enter(3.50, 10)
    position.exit(4.50)

    assert position.exit_price == 4.50
    assert position.size == 0

def test_position_enter_short(position):
    position.enter(3.50, -10)

    assert position.entry_price == 3.50
    assert position.size == -10

def test_position_exit_pnl(position):
    position.enter(3.50, 10)
    position.exit(4.00)

    assert position.pnl() == 5

