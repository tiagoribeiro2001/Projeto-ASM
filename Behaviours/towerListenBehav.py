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

            # Torre de controlo contacta o gestor de gares para verificar se existe uma gare livre
            request_gare = Message(to="gare@" + XMPP_SERVER)
            request_gare.set_metadata("performative", "request_gare")
            request_gare.body = f"{type}"
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
                    print(f"Tower manager informing which gare the plane is going to use to gare manager...")
                    await self.send(gare_occupy)

                    # Envia a mensagem de confirmacao para o aviao
                    response_plane = Message(to=str(msg.sender))
                    response_plane.set_metadata("performative", "landing_authorized")
                    landing_info = {"runway": runway,
                                    "gare": gare}
                    json_data = jsonpickle.encode(landing_info)
                    response_plane.body = json_data
                    await self.send(response_plane)

                # Nao existem pistas livres
                else:
                    # Envia a mensagem ao aviao a dizer que nao ha pistas disponiveis e tera que aguardar

                    # FALTA A PARTE DE POR O AVIAO NA LISTA DE ESPERA


                    response = Message(to=msg.sender)
                    response.body = "Landing not authorized. No runway available."
                    await self.send(response)
                    
            # Se receber que nao existem gares
            elif toDo == "no_free_gares":
                # Envia a mensagem de negacao
                response = Message(to=msg.sender)
                response.body = "Landing not authorized. No parking available."
                await self.send(response)

        elif toDo == "takeoff_request":
            # Processa a mensagem e verifica se ha espaço disponivel para levantar
            print(f"Takeoff request received from {msg.sender}. Aircraft: {msg.body}")

            if available_runway:
                # Envia a mensagem de confirmacao
                response = Message(to=msg.sender)
                response.body = "Takeoff authorized. Runway available."
                await self.send(response)

            else:
                # Envia a mensagem de negacao
                response = Message(to=msg.sender)
                response.body = "Takeoff not authorized. No runway available."
                await self.send(response)
