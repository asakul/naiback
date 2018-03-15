
from .strategy import Strategy
from ..data.bars import Bars
from ..exceptions import NaibackException

class SingleAssetStrategy(Strategy):

    def __init__(self):
        super.__init__()
        self.bars = None

    def run(self, from_time=None, to_time=None):
        self._prepare_bars()
        super.run(from_time, to_time)

    def _prepare_bars(self):
        if len(self.feeds) == 0:
            raise NaibackException('No feeds added to strategy')

        self.bars = list(Bars.from_feed(self.feeds[0]))
