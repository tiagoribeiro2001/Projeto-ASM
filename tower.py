from spade.agent import Agent
from airstrip import Airstrip


class TowerAgent(Agent):
    
    async def setup(self):
        print("Tower Agent {}".format(str(self.jid)) + "starting...")

        avioes = []
        
        p1 = Airstrip(490, 490, True)
        p2 = Airstrip(510, 510, True)
        p3 = Airstrip(490, 510, True)
        p4 = Airstrip(510, 490, True)
        pistas = [p1, p2, p3, p4]