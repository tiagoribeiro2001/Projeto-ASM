from spade.agent import Agent

class ManagerAgent(Agent):
    
    async def setup(self):
        print("Manager Agent {}".format(str(self.jid)) + "starting...")

        avioes = []
        pistas = []
