from spade.agent import Agent
from Behaviours.managerRequestBehav import ManagerRequestBehav

class ManagerAgent(Agent):
    
    async def setup(self):
        print("Manager Agent {}".format(str(self.jid)) + " starting...")

        self.landingQueue = []
        self.takeoffQueue = []
        self.planesLanding = []
        self.planesTakeoff = []

        #avioes = []
        #pistas = []
        '''self.avioes = {}
        self.pistas = {}
        self.aterragem_queue = []
        self.descolagem_queue = []
        self.max_fila_aterragem = 10
        self.max_fila_descolagem = 10
        '''

        a = ManagerRequestBehav(period=10.0)
        self.add_behaviour(a)   