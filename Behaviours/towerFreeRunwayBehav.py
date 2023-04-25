from spade.behaviour import OneShotBehaviour
from spade.message import Message
from dados import XMPP_SERVER
import jsonpickle
import math

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

class TowerFreeRunwayBehav(OneShotBehaviour):

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data

    async def run(self):

        # Liberta a pista
        self.agent.runways[self.data]["status"] = "free"
        print(f"Runway {str(self.data)} is now free")
        
        # Percorrer a lista de espera de aterragens
        for plane in self.agent.landingQueue:

            # Verifica se existe alguma gare para o tipo de avião que está a iterar
            available_gares = Message(to="gare@" + XMPP_SERVER)
            available_gares.set_metadata("performative", "available_gares")
            json_data = jsonpickle.encode(plane["type"])
            available_gares.body = json_data
            await self.send(available_gares)

            gare_response = await self.receive(timeout=1000)
            toDo = gare_response.get_metadata("performative")
            print(f"Control tower received from gare manager: {toDo}")

            if toDo == "available_gares_response":

                gare_list = jsonpickle.decode(gare_response.body)

                # Verifica que a lista não veio vazia
                if gare_list:

                    runway, gare = shortest_path(self.agent.runways, gare_list)

                    if runway or gare:

                        plane_msg = Message(to=str(plane["id"]))
                        plane_msg.set_metadata("performative", "landing_authorized")
                        landing_info = {"runway": runway,
                                    "gare": gare}
                        plane_msg.body = jsonpickle.encode(landing_info)
                        await self.send(plane_msg)
        
        # Percorre a lista de espera de descolagens
        for plane in self.agent.takeoffQueue:

            runway = closest_runway(self.agent.runways, plane["gare"])

            if runway:
                
                plane_msg = Message(to=str(plane["id"]))
                plane_msg.set_metadata("performative", "takeoff_authorized")
                takeoff_info = {"runway": runway}
                plane_msg.body = jsonpickle.encode(takeoff_info)
                await self.send(plane_msg)