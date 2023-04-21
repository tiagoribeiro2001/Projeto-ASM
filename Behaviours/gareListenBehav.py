import math
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from dados import XMPP_SERVER, PASSWORD
import jsonpickle

# Verifica se existe alguma pista disponível para um certo tipo de aviao e devolve um dicionario destas
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

                # Gares disponiveis
                free_gares = available_gares(type)

                # Se houver gares disponíveis
                if free_gares:
                    # Codifica o dicionario de gares disponiveis
                    json_data = jsonpickle.encode(free_gares)
                    
                    # manda a resposta
                    response = Message(to=msg.sender)
                    response.set_metadata("performative", "free_gares")
                    response.body = json_data
                    print(f"Gare manager sending tower manager the free gares...")
                    await self.send(response)

                # Se não houver gares disponíveis
                else:

                    response = Message(to="tower@" + XMPP_SERVER)
                    response.set_metadata("performative", "no_free_gares")
                    response.body = "There are no free gares."
                    print(f"Gare manager sending tower manager that there are no free gares...")
                    await self.send(response)
