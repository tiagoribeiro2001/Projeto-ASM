import math
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from dados import XMPP_SERVER, PASSWORD
import jsonpickle

# Verifica se existe alguma pista disponível 
def available_gares(self, type):
    available = {}
    for key, value in self.gares.items():
        if value["type"] == type and value["status"] == "free":
            available[key] = value
    return available

class gareListenBehav(OneShotBehaviour):

    async def run(self):
        while True:
            # Recebe a mensagem
            msg = await self.receive(timeout=1000)
            toDo = msg.get_metadata("performative")
            print(f"Manager gare received: {toDo}")

            if toDo == "request_gate" :
                type = msg.body
                free_gares = available_gares(type)
                json_data = jsonpickle.encode(free_gares)
                
                # manda a resposta
                
                
