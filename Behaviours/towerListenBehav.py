import math
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from dados import XMPP_SERVER
from towerLandingBehav import TowerLandingBehav
import jsonpickle

def closest_runway(runways, gare):
    best_runway = None
    min_dist = 1000
    for key, value in runways.items():
        if value["status"] == "free":
            dist = distance(value["location"], gare)
            if dist < min_dist:
                best_runway = key
                min_dist = dist
    return best_runway

class towerListenBehav(CyclicBehaviour):

    async def run(self):
        # Recebe a mensagem
        msg = await self.receive(timeout=1000)
        toDo = msg.get_metadata("performative")
        print(f"Control Tower received: {toDo}")

        # Recebe pedido de aviao a querer aterrar
        if toDo == "landing_request":

            # processa a mensagem e verifica se há espaço disponível para aterrar
            print(f"Landing request received from {msg.sender}. Aircraft: {msg.body}")
            json_data = msg.body
            plane_info = jsonpickle.decode(json_data)

            a = TowerLandingBehav(plane_info)
            self.agent.add_behaviour(a)

        # Recebe pedido de aviao a querer levantar voo
        elif toDo == "takeoff_request":
            # Processa a mensagem e verifica se ha espaço disponivel para levantar voo
            print(f"Takeoff request received from {msg.sender}. Aircraft: {msg.body}")
            json_data = msg.body
            plane_info = jsonpickle.decode(json_data)

            # Se existirem pistas disponiveis
            if available_runway(self.agent.runways):

                plane_gare = plane_info["gare"]
                json_data = jsonpickle.encode(plane_gare)

                # Envia mensagem ao gestor de gares para obter informacoes da gare atual do aviao
                gare_location = Message(to="gare@" + XMPP_SERVER)
                gare_location.set_metadata("performative", "gare_location")
                gare_location.body = json_data
                await self.send(gare_location)

                # Recebe a resposta do gestor de gares com a localizacao da gare
                gare_response = await self.receive(timeout=1000)
                toDo = gare_response.get_metadata("performative")
                print(f"Control tower received from gare manager: {toDo}")
                json_data = gare_response.body
                gare_loc = jsonpickle.decode(json_data)
                print(f"Control tower has the location where {str(msg.sender)} is located.")

                # Calcula a pista mais proxima da gare do aviao
                runway = closest_runway(self.agent.runways, gare_loc)
                
                # Envia a mensagem de confirmacao de descolagem ao aviao
                json_data = jsonpickle.encode(runway)
                response_plane = Message(to=str(msg.sender))
                response_plane.set_metadata("performative", "takeoff_authorized")
                response_plane.body = json_data
                await self.send(response_plane)

                # Desocupa a pista
                plane_takeoff = await self.receive(timeout=1000)
                toDo = plane_takeoff.get_metadata("performative")
                print(f"Control tower received from plane: {toDo}")
                json_data = plane_takeoff.body
                free_runway = jsonpickle.decode(json_data)
                self.agent.runways[free_runway]["status"] = "free"
                print(f"Runway {str(free_runway)} is now free")

            else:
                # Adiciona a lista de espera de descolagens
                self.agent.takeoffQueue[plane_info["id"]] = plane_info

                # Envia a mensagem de negacao
                response = Message(to=str(msg.sender))
                response_plane.set_metadata("performative", "takeoff_not_authorized")
                response.body = "Takeoff not authorized. No runway available. Added to the takeoff queue."
                await self.send(response)
