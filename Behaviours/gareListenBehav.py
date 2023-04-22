from spade.behaviour import CyclicBehaviour
from spade.message import Message
from dados import XMPP_SERVER
import jsonpickle

# Verifica se existe alguma pista disponível para um certo tipo de aviao e devolve um dicionario destas
def available_gares(gares, type):
    available = {}
    for key, value in gares.items():
        if value["type"] == type and value["status"] == "free":
            available[key] = value
    return available

class gareListenBehav(CyclicBehaviour):

    async def run(self):
        # Recebe a mensagem
        msg = await self.receive(timeout=1000)
        toDo = msg.get_metadata("performative")
        print(f"Manager gare received: {toDo}")

        if toDo == "request_gare":
            json_data = msg.body
            type = jsonpickle.decode(json_data)

            # Gares disponiveis
            free_gares = available_gares(self.agent.gares, type)

            # Se houver gares disponíveis
            if free_gares:
                # Codifica o dicionario de gares disponiveis
                json_data = jsonpickle.encode(free_gares)
                
                # Manda as gares disponiveis para a torre de controlo
                response = Message(to=str(msg.sender))
                response.set_metadata("performative", "free_gares")
                response.body = json_data
                print(f"Gare manager sending control tower the free gares...")
                await self.send(response)

                # Espera resposta da torre de controlo
                response_tower = await self.receive(timeout=1000)
                toDo = response_tower.get_metadata("performative")
                print(f"Manager gare received: {toDo}")

                if toDo == "gare_occupy":
                    json_data = response_tower.body
                    occupied_gare = jsonpickle.decode(json_data)
                    self.agent.gares[occupied_gare]["status"] = "occupied"
                    print(f"Gare {occupied_gare} occupied ...")


            # Se não houver gares disponíveis
            else:
                response = Message(to=str(msg.sender))
                response.set_metadata("performative", "no_free_gares")
                response.body = "There are no free gares."
                print(f"Gare manager sending tower manager that there are no free gares...")
                await self.send(response)
        
        # Recebe a mensagem da torre de controlo a pedir a localizacao da gare
        elif toDo == "gare_location":

            json_data = msg.body
            gare = jsonpickle.decode(json_data)

            # Vai buscar a localizacao da gare
            gare_location = self.agent.gares[gare]["location"]

            # Envia a localizacao da gare para a torre de controlo
            json_data = jsonpickle.encode(gare_location)
            response = Message(to=str(msg.sender))
            response.set_metadata("performative", "gare_response")
            response.body = json_data
            print(f"Gare manager sent gare location to control tower.")
            await self.send(response)

       

