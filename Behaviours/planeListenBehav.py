from spade.behaviour import CyclicBehaviour
from spade.message import Message
from dados import XMPP_SERVER
import jsonpickle

class PlaneListenBehav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1000)
        toDo = msg.get_metadata("performative")
        print(f"Plane received: {toDo}")

