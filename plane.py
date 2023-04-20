from spade.agent import Agent
import random

class PlaneAgent(Agent):

    def __init__(self, company, type, origin, destiny):
        self.company = company
        self.type = type
        self.origin = origin
        self.destiny = destiny

    async def setup(self):
        print("Plane Agent {}".format(str(self.jid)) + "starting...")
        self.id = self.jid

