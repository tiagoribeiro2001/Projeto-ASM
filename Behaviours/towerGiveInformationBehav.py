from spade.behaviour import OneShotBehaviour
from spade.message import Message
from dados import XMPP_SERVER
import jsonpickle


class TowerGiveInformationBehav(OneShotBehaviour):

    async def run(self):

        json_data = jsonpickle.encode(plane_info)
        

        # Envia mensagem ao manager as informacoes 
        gare_location_request = Message(to="gare@" + XMPP_SERVER)
        gare_location_request.set_metadata("performative", "gare_location_request")
        gare_location_request.body = json_data
        await self.send(gare_location_request)
