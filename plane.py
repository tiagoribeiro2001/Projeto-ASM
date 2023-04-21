from spade.agent import Agent
from Behaviours.planeStartBehav import PlaneStartBehav
from Behaviours.landingRequestBehav import LandingRequestBehav
import random

class PlaneAgent(Agent):

    async def setup(self):
        companies = ["RyanAir", "EasyJet", "TAP", "Emirates", "Qatar Airways", "Turkish Airlines", "Etihad Airways"]
        types = ["cargo", "comercial"]
        origins = ["Porto", "Lisboa", "Madrid", "Barcelona", "Paris", "Marselha"]
        destinies = list(origins)

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