import math
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from dados import XMPP_SERVER
import jsonpickle

#distance between two points
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Verifica se existe alguma pista disponível 
def available_runway(self):
    for runway in self.runways.items():
        if runway["status"] == "free":
            return True
    return False

# Verifica o menor caminho
def shortest_path(self, gares):
    best_runway = None
    best_gare = None
    min_dist = 1000
    for runway in self.runways.items():
        if runway["status"] == "free":
            for gare in gares:
                dist = distance(runway["location"], gare["location"])
                if dist < min_dist:
                    best_runway = runway.key()
                    best_gare = gare.key()
                    min_dist = dist
    return (best_runway, best_gare)

class towerListenBehav(OneShotBehaviour):

    async def run(self):
        while True:
            # Recebe a mensagem
            msg = await self.receive(timeout=1000)
            toDo = msg.get_metadata("performative")
            print(f"Manager tower received: {toDo}")

            # Recebe pedido de aviao a querer aterrar
            if toDo == "aviao_aterrar":

                # processa a mensagem e verifica se há espaço disponível para aterrar
                print(f"Landing request received from {msg.sender}. Aircraft: {msg.body}")
                info = msg.body.split("|")
                type = info[2]

                # Torre de controlo contacta o gestor de gares para verificar se existe uma gare livre
                request_gare = Message(to="gare@" + XMPP_SERVER)
                request_gare.set_metadata("performative", "request_gare")
                request_gare.body = f"{type}"
                print(f"Tower manager contacting gare manager to check if there are any available gares...")
                await self.send(request_gare)

                # Recebe a resposta do gestor de gares
                response_gare = await self.receive(timeout=1000)
                toDo = response_gare.get_metadata("performative")
                print(f"Manager tower received: {toDo}")

                # Se receber que existem gares livres
                if toDo == "free_gares":
                    
                    # Depois de confirmada a existência de gares verifica se há pistas livres para aterragem 
                    if available_runway:
                        # Calcula o caminho mais curto das pistas e gares disponiveis
                        json_data = msg.body
                        free_gares = jsonpickle.decode(json_data)
                        info = shortest_path(free_gares)

                        # Envia a mensagem de confirmação
                        response = Message(to=msg.sender)
                        response.body = f"Landing authorized. Runway and parking available. Runway: {info[0].key()}. Gare: {info[1].key()}."
                        await self.send(response)
                        
                        # Envia a mensagem de ocupação da gare
                        #response = Message("to=gare@" + XMPP_SERVER)
                        #request_gare.set_metadata("performative", "ocupation_gare")
                        #request_gare.body = f"{info[0].key()}"
                        #print(f"Tower manager informing witch gare is using to gare manager...")
                        #await self.send(request_gare)

                    # Nao existem pistas livres
                    else:
                        # Envia a mensagem ao aviao a dizer que nao ha pistas disponiveis e tera que aguardar

                        # FALTA A PARTE DE POR O AVIAO NA LISTA DE ESPERA


                        response = Message(to=msg.sender)
                        response.body = "Landing not authorized. No runway available."
                        await self.send(response)
                        
                # Se receber que nao existem gares
                elif toDo == "no_free_gares":
                    # Envia a mensagem de negação
                    response = Message(to=msg.sender)
                    response.body = "Landing not authorized. No parking available."
                    await self.send(response)

                    



            # elif toDo == "aviao_descolar":
            #     # processa a mensagem e verifica se há espaço disponível para levantar
            #     print(f"TakeOff request received from {msg.sender}. Aircraft: {msg.body}")
            #     if available_runway and available_parking:
            #         # envia a mensagem de confirmação
            #         response = Message(to=msg.sender)
            #         response.body = "Landing authorized. Runway and parking available."
            #         await self.send(response)
            #     else:
            #         # envia a mensagem de negação
            #         response = Message(to=msg.sender)
            #         response.body = "Landing not authorized. No runway or parking available."
            #         await self.send(response)
