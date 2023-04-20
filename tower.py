from spade.agent import Agent
from Behaviours.landingRequestBehav import LandingRequestBehav

class TowerAgent(Agent):
    
    async def setup(self):
        print("Tower Agent {}".format(str(self.jid)) + "starting...")
    
        avioes = []

        self.runways = {
            "r1": {"location": (400, 400), "status": "free"},
            "r2": {"location": (600, 400), "status": "free"},
            "r3": {"location": (600, 600), "status": "free"},
            "r4": {"location": (400, 600), "status": "free"}
        }
        
         

        a = LandingRequestBehav()
        self.add_behaviour(a)