
from siren_sprinkler import SirenSprinkler

class SirenStation(object):
    def __init__(self, app_context, name, addr):
        self.name = name
        self.addr = addr
        self.app_context = app_context
        self.sprinklers = []
