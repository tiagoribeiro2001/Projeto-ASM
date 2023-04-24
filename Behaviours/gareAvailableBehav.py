from spade.behaviour import OneShotBehaviour
from spade.message import Message
from dados import XMPP_SERVER
import jsonpickle
import math

def available_gares(gares, type):
    available = {}
    for key, value in gares.items():
        if value["type"] == type and value["status"] == "free":
            available[key] = value
    return available

class GareAvailableBehav(OneShotBehaviour):

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data

    async def run(self):

        gare_list = available_gares(self.agent.gares, self.data)

        available_gares_response = Message(to="gare@" + XMPP_SERVER)
        available_gares_response.set_metadata("performative", "available_gares_response")
        json_data = jsonpickle.encode(gare_list)
        available_gares_response.body = json_data
        await self.send(available_gares_response)
        