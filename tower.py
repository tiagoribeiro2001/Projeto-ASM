from spade.agent import Agent
from Behaviours.towerListenBehav import towerListenBehav

class TowerAgent(Agent):
    
    async def setup(self):
        print("Tower Agent {}".format(str(self.jid)) + " starting...")
    
        landingQueue = {}
        #max_queue_size = 10

        takeoffQueue = {}
        
        self.runways = {
            "r1": {"location": (400, 400), "status": "free"},
            "r2": {"location": (600, 400), "status": "free"},
            "r3": {"location": (600, 600), "status": "free"},
            "r4": {"location": (400, 600), "status": "free"}
        }
        
        a = towerListenBehav()
        self.add_behaviour(a)