import math
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from dados import XMPP_SERVER
import jsonpickle

#distance between two points
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Verifica se existe alguma pista disponível 
def available_runway(runways):
    for key, value in runways.items():
        if value["status"] == "free":
            return True
    return False

# Verifica o menor caminho entre as pistas e gares disponiveis
def shortest_path(runways, gares):
    best_runway = None
    best_gare = None
    min_dist = 1000
    for key1, value1 in runways.items():
        if value1["status"] == "free":
            for key2, value2 in gares.items():
                dist = distance(value1["location"], value2["location"])
                if dist < min_dist:
                    best_runway = key1
                    best_gare = key2
                    min_dist = dist
    return (best_runway, best_gare)

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

            type = plane_info["type"]
            json_data = jsonpickle.encode(type)

            # Torre de controlo contacta o gestor de gares para verificar se existe uma gare livre
            request_gare = Message(to="gare@" + XMPP_SERVER)
            request_gare.set_metadata("performative", "request_gare")
            request_gare.body = json_data
            print(f"Control tower contacting gare manager to check if there are any available gares...")
            await self.send(request_gare)

            # Recebe a resposta do gestor de gares
            response_gare = await self.receive(timeout=1000)
            toDo = response_gare.get_metadata("performative")
            print(f"Control tower received from gare manager: {toDo}")

            # Se receber que existem gares livres
            if toDo == "free_gares":
                
                # Depois de confirmada a existencia de gares verifica se ha pistas livres para aterragem 
                if available_runway(self.agent.runways):

                    # Calcula o caminho mais curto das pistas e gares disponiveis
                    json_data = response_gare.body
                    free_gares = jsonpickle.decode(json_data)
                    info = shortest_path(self.agent.runways, free_gares)

                    # Pista escolhida para aterrar
                    runway = info[0]
                    # Gare escolhida para estacionar
                    gare = info[1]

                    # Altera o estado da pista
                    self.agent.runways[runway]["status"] = "occupied"
                    print(f"Runway {runway} occupied ...")

                    # Envia a mensagem de ocupacao da gare para o gestor de gares
                    gare_occupy = Message(to=str(response_gare.sender))
                    gare_occupy.set_metadata("performative", "gare_occupy")
                    json_data = jsonpickle.encode(gare)
                    gare_occupy.body = json_data
                    print(f"Control tower informing which gare the plane is going to use to gare manager...")
                    await self.send(gare_occupy)

                    # Envia a mensagem de confirmacao para o aviao
                    response_plane = Message(to=str(msg.sender))
                    response_plane.set_metadata("performative", "landing_authorized")
                    landing_info = {"runway": runway,
                                    "gare": gare}
                    json_data = jsonpickle.encode(landing_info)
                    response_plane.body = json_data
                    print(f"Control tower sending landing confirmation to {str(msg.sender)}")
                    await self.send(response_plane)

                    # Recebe a resposta de aterragem do avião e liberta a pista
                    plane_landing = await self.receive(timeout=1000)
                    toDo = plane_landing.get_metadata("performative")
                    print(f"Control tower received from plane: {toDo}")
                    json_data = plane_landing.body
                    free_runway = jsonpickle.decode(json_data)
                    self.agent.runways[free_runway]["status"] = "free"
                    print(f"Runway {str(free_runway)} is now free")


                # Nao existem pistas livres
                else:
                    # Adiciona a lista de espera de aterragens
                    self.agent.landingQueue[plane_info["id"]] = plane_info

                    # Envia a mensagem ao aviao a dizer que nao ha pistas disponiveis e tera que aguardar
                    response = Message(to=str(msg.sender))
                    response.set_metadata("performative", "landing_not_authorized")
                    response.body = "Landing not authorized. No runway available. Added to the landing queue."
                    await self.send(response)
                    
            # Se receber que nao existem gares
            elif toDo == "no_free_gares":
                # Envia a mensagem de negacao
                response = Message(to=str(msg.sender))
                response.body = "Landing not authorized. No parking available."
                await self.send(response)

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
