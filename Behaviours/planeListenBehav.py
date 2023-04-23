from spade.behaviour import CyclicBehaviour
from Behaviours.planeLandingBehav import PlaneLandingBehav
from Behaviours.planeTakeoffBehav import PlaneTakeoffBehav
import jsonpickle

class PlaneListenBehav(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=1000)
        toDo = msg.get_metadata("performative")
        print(f"Plane received: {toDo}")

        # Aterragem autorizada 
        if toDo == "landing_authorized":
            json_data = msg.body
            mensagem = jsonpickle.decode(json_data)

            a = PlaneLandingBehav(mensagem)
            self.agent.add_behaviour(a)

        # Aterragem nao autorizada
        elif toDo == "landing_not_authorized":
            pass
    
        # Descolagem autorizada
        elif toDo == "takeoff_authorized":
            json_data = msg.body
            mensagem = jsonpickle.decode(json_data)

            a = PlaneTakeoffBehav(mensagem)
            self.agent.add_behaviour(a)

        # Descolagem nao autorizada
        elif toDo == "takeoff_not_authorized":
            pass