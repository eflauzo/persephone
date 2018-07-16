
import time

class AppContext(object):

    def __init__(self):
        self.application = None
        self.config = None
        self.can_interface = None
        self.canstruct = None

    def time(self):
        """This can be overriden for testing"""
        return time.time()
