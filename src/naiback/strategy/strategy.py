from abc import abstractmethod

class Strategy:
    """
    Internal base class for strategies. User should use it's subclasses (i.e. SingleAssetStrategy)
    """

    def __init__(self):
        self.feeds = []

    def add_feed(self, feed):
        """
        Adds feed to feeds list.
        """
        self.feeds.append(feed)

    @abstractmethod
    def execute(self):
        """
        Will be called by 'run'
        """
        pass

    def run(self, from_time=None, to_time=None):
        """
        By default, just calls execute.
        """
        self.execute()
