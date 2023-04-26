from spade.behaviour import OneShotBehaviour
from spade.message import Message
from dados import XMPP_SERVER
import jsonpickle


class TowerGiveInformationBehav(OneShotBehaviour):

    async def run(self):
        data = jsonpickle.encode({
            "action": "update_info",
            "landingQueue": self.agent.landingQueue,
            "takeoffQueue": self.agent.takeoffQueue,
            "planesLanding": self.agent.planesLanding,
            "planesTakeoff": self.agent.planesTakeoff
        })
        # Envia mensagem ao manager as informacoes 
        gare_location_request = Message(to="gare@" + XMPP_SERVER)
        gare_location_request.set_metadata("performative", "gare_location_request")
        gare_location_request.body = data
        await self.send(gare_location_request)
