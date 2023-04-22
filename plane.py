from spade.agent import Agent
from Behaviours.planeStartBehav import PlaneStartBehav
from Behaviours.landingRequestBehav import LandingRequestBehav
from Behaviours.takeoffRequestBehav import TakeoffRequestBehav
import random

class PlaneAgent(Agent):

    async def setup(self):
        state = ["air", "ground"]
        companies = ["RyanAir", "EasyJet", "TAP", "Emirates", "Qatar Airways", "Turkish Airlines", "Etihad Airways"]
        types = ["cargo", "commercial"]
        origins = ["Porto", "Lisboa", "Madrid", "Barcelona", "Paris", "Marselha"]
        destinies = list(origins)

        self.state = random.choice(state)
        self.runway = None
        self.gare = None

        # Tempo que demora a aterrar e que fica no aeroporto (podemos meter random)
        self.landingTime = 5
        self.groundTime = 5


        self.company = random.choice(companies)
        self.type = random.choice(types)
        self.origin = random.choice(origins)
        destinies.remove(self.origin)  # remove a origem da lista de destinos
        self.destiny = random.choice(destinies)

        print("Plane Agent {}".format(str(self.jid)) + "starting...")

        a = PlaneStartBehav()
        self.add_behaviour(a)

        b = LandingRequestBehav()
        self.add_behaviour(b)

        c = TakeoffRequestBehav()
        self.add_behaviour(c)