from spade.behaviour import OneShotBehaviour
from spade.message import Message
from dados import XMPP_SERVER
import jsonpickle
import asyncio

class PlaneLandingBehav(OneShotBehaviour):

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data

    async def run(self):

        self.agent.runway = self.data["runway"]
        self.agent.gare = self.data["gare"]

        # Espera o tempo que demora a aterrar
        print(f"Plane {str(self.agent.jid)} starting the landing")
        await asyncio.sleep(self.agent.landingTime)
        
        # Espera o tempo que fica na pista
        print(f"Plane {str(self.agent.jid)} has landed in runway {str(self.agent.runway)}")
        self.agent.state = "ground"
        await asyncio.sleep(self.agent.runwayTime)

        # Envia mensagem à torre de controlo para desocupar a pista
        response = Message(to="tower@" + XMPP_SERVER)
        response.set_metadata("performative", "free_runway")
        json_data = jsonpickle.encode(self.agent.runway)
        response.body = json_data
        await self.send(response)
        print(f"Plane {str(self.agent.jid)} indicating control tower that the runway {str(self.agent.runway)} is free...")

        # Espera o tempo de viagem desde a pista ate a gare
        print(f"Plane {str(self.agent.jid)} going from runway {str(self.agent.runway)} to gare {str(self.agent.gare)}.")
        await asyncio.sleep(self.agent.moveTime)

        # Altera o estado do aviao para parkado
        print(f"Plane {str(self.agent.jid)} reached gare {str(self.agent.gare)}. The plane is now parked.")
        self.agent.state = "parked"


        # Envia mensagem à torre de controlo para desocupar a pista
        # Obtem informacoes do voo
        plane_info = {"id": str(self.agent.jid),
                      "state": self.agent.state,
                      "company": self.agent.company,
                      "type": self.agent.type,
                      "origin": self.agent.origin,
                      "destiny": self.agent.destiny,
                      "runway": self.agent.runway,
                      "gare": self.agent.gare,
                      "waitTime": str(self.agent.waitTime),
                      "landingTime": str(self.agent.landingTime),
                      "runwayTime": str(self.agent.runwayTime),
                      "moveTime": str(self.agent.moveTime)
                      }
        json_data = jsonpickle.encode(plane_info)

        response = Message(to="tower@" + XMPP_SERVER)
        response.set_metadata("performative", "free_plane_landing")
        response.body = json_data
        await self.send(response)


