import math
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from dados import XMPP_SERVER, PASSWORD

#distance between two points
def distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

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
                dist = distance(runway[""])
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

            # Verifica 
            if toDo == "aviao_aterrar":
                
                # processa a mensagem e verifica se há espaço disponível para aterrar
                print(f"Landing request received from {msg.sender}. Aircraft: {msg.body}")
                info = msg.body.split("|")
                type = info[2]

                if available_runway:
                    
                    # Torre de controlo contacta o gestor de gares para verificar se existe uma gare livre
                    msg = Message(to="gare@" + XMPP_SERVER)
                    msg.set_metadata("performative", "request_gare")
                    msg.body = f"{type}"
                    print(f"Tower manager requesting gare to gare manager...")
                    await self.send(msg)

                    # Recebe a resposta do gestor de gares
                    msg = await self.receive(timeout=1000)
                    toDo = msg.get_metadata("performative")
                    print(f"Manager tower received: {toDo}")

                    if toDo == "free_gares":
                        # Calcula o caminho mais curto das pistas e gares disponiveis
                        free_gares = msg.body




                        # envia a mensagem de confirmação
                        # FALTA ENVIAR A PISTA E GARE A ATERRAR
                        response = Message(to=msg.sender)
                        response.body = "Landing authorized. Runway and parking available."
                        await self.send(response)

                    elif toDo == "no_free_gares":
                        # envia a mensagem de negação
                        response = Message(to=msg.sender)
                        response.body = "Landing not authorized. No parking available."
                        await self.send(response)


                    
                else:
                    # envia a mensagem de negação
                    response = Message(to=msg.sender)
                    response.body = "Landing not authorized. No runway available."
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






