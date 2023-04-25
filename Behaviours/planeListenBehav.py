from spade.behaviour import CyclicBehaviour
from Behaviours.planeLandingBehav import PlaneLandingBehav
from Behaviours.planeTakeoffBehav import PlaneTakeoffBehav
from Behaviours.planeTimeoutBehav import PlaneTimeoutBehav
import jsonpickle

class PlaneListenBehav(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=1000)
        toDo = msg.get_metadata("performative")
        
        # Aterragem autorizada 
        if toDo == "landing_authorized":
            print(f"Plane received: {toDo}")
            json_data = msg.body
            mensagem = jsonpickle.decode(json_data)

            a = PlaneLandingBehav(mensagem)
            self.agent.add_behaviour(a)

        # Aterragem nao autorizada
        elif toDo == "landing_not_authorized":
            print(f"Plane received: {toDo}")

            message = await self.receive(timeout=self.agent.waitTime)

            if message == None:
                a = PlaneTimeoutBehav()
                self.agent.add_behaviour(a)

    
        # Descolagem autorizada
        elif toDo == "takeoff_authorized":
            print(f"Plane received: {toDo}")
            json_data = msg.body
            mensagem = jsonpickle.decode(json_data)

            a = PlaneTakeoffBehav(mensagem)
            self.agent.add_behaviour(a)

        # Descolagem nao autorizada
        elif toDo == "takeoff_not_authorized":
            print(f"Plane received: {toDo}")

        # Aterragem nao autorizada e fila de espera cheia
        elif toDo == "full_landing_queue":
            print(f"Plane received: {toDo}. Finding another airport.")
            self.agent.stop()
            