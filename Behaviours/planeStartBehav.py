from spade.behaviour import OneShotBehaviour
from spade.message import Message
from dados import XMPP_SERVER

class PlaneStartBehav(OneShotBehaviour):

    async def run(self):
        msg = Message(to="tower@" + XMPP_SERVER)
        msg.set_metadata("performative", "plane_subscribe")
        msg.body = f"{str(self.agent.jid)}"
        print(f"Plane subscribing to tower")
        await self.send(msg)
        