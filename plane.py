from spade.agent import Agent
from Behaviours.planeListenBehav import PlaneListenBehav
from Behaviours.landingRequestBehav import LandingRequestBehav
from Behaviours.takeoffRequestBehav import TakeoffRequestBehav
import random

class PlaneAgent(Agent):

    async def setup(self):
        state = ["air", "ground", "parked"]
        companies = ["RyanAir", "EasyJet", "TAP", "Emirates", "Qatar Airways", "Turkish Airlines", "Etihad Airways"]
        types = ["cargo", "commercial"]
        origins = ["Porto", "Lisboa", "Madrid", "Barcelona", "Paris", "Marselha"]
        destinies = list(origins)

        self.state = random.choice(state)
        self.runway = None
        self.gare = "g1"

        # Tempo que demora a aterrar e que fica no aeroporto (podemos meter random)
        self.waitTime = 5
        self.landingTime = 5
        self.runwayTime = 5
        self.moveTime = 5

        self.company = random.choice(companies)
        self.type = random.choice(types)
        self.origin = random.choice(origins)
        destinies.remove(self.origin)  # remove a origem da lista de destinos
        self.destiny = random.choice(destinies)

        print("Plane Agent {}".format(str(self.jid)) + " starting...")

        b = PlaneListenBehav()
        self.add_behaviour(b)

        # c = LandingRequestBehav()
        # self.add_behaviour(c)

        d = TakeoffRequestBehav()
        self.add_behaviour(d)