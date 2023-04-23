from spade.behaviour import CyclicBehaviour
from Behaviours.towerLandingBehav import TowerLandingBehav
from Behaviours.towerTakeoffBehav import TowerTakeoffBehav
import jsonpickle



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

            a = TowerTakeoffBehav(plane_info)
            self.agent.add_behaviour(a)
            
