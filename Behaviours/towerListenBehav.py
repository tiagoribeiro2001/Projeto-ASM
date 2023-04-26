from spade.behaviour import CyclicBehaviour
from Behaviours.towerLandingBehav import TowerLandingBehav
from Behaviours.towerTakeoffBehav import TowerTakeoffBehav
from Behaviours.towerFreeRunwayBehav import TowerFreeRunwayBehav
from Behaviours.towerTimeoutBehav import TowerTimeoutBehav
from Behaviours.towerGiveInformationBehav import TowerGiveInformationBehav
import jsonpickle


class towerListenBehav(CyclicBehaviour):

    async def run(self):
        # Recebe a mensagem
        msg = await self.receive(timeout=1000)
        toDo = msg.get_metadata("performative")
        

        # Recebe pedido de aviao a querer aterrar
        if toDo == "landing_request":
            print(f"Control Tower received: {toDo}")

            # processa a mensagem e verifica se há espaço disponível para aterrar
            print(f"Landing request received from {msg.sender}. Aircraft: {msg.body}")
            json_data = msg.body
            plane_info = jsonpickle.decode(json_data)

            a = TowerLandingBehav(plane_info)
            self.agent.add_behaviour(a)

        # Recebe pedido de aviao a querer levantar voo
        elif toDo == "takeoff_request":
            print(f"Control Tower received: {toDo}")
            
            # Processa a mensagem e verifica se ha espaço disponivel para levantar voo
            print(f"Takeoff request received from {msg.sender}. Aircraft: {msg.body}")
            json_data = msg.body
            plane_info = jsonpickle.decode(json_data)

            a = TowerTakeoffBehav(plane_info)
            self.agent.add_behaviour(a)

        # Recebe pedido de aviao para esvaziar a pista
        elif toDo == "free_runway":
            print(f"Control Tower received: {toDo}")

            # Processa a mensagem e verifica se ha espaço disponivel para levantar voo
            print(f"Free runway request received from {msg.sender}. Runway: {msg.body}")
            json_data = msg.body
            runway = jsonpickle.decode(json_data)

            a = TowerFreeRunwayBehav(runway)
            self.agent.add_behaviour(a)
        
        # Recebe pedido de aviao a dizer esperou o tempo maximo na fila de espera
        elif toDo == "time_out":
            print(f"Control Tower received: {toDo}")

            print(f"Time out request received from {msg.sender}.")
            json_data = msg.body
            id = jsonpickle.decode(json_data)

            a = TowerTakeoffBehav(id)
            self.agent.add_behaviour(a)

        # Recebe pedido para dar display das informações
        elif toDo == "request_information":
            print(f"Control Tower received: {toDo}")

            print(f"Information request received from manager.")
            
            a = TowerGiveInformationBehav()
            self.agent.add_behaviour(a)   

        elif toDo == "free_plane_landing":
            print(f"Control Tower received: {toDo}")
            print("Update the list of planes landing...")
            json_data = msg.body
            plane = jsonpickle.decode(json_data)

            # Remove aviao da lista das aterragens
            for plane in self.agent.planesLanding:
                if plane["id"] == str(msg.sender):
                    self.agent.planesLanding.remove(plane)
                    print(f"Control tower removed plane {msg.sender} from the planes landing list.")
            

        elif toDo == "free_plane_takeoff":
            print(f"Control Tower received: {toDo}")
            print("Update the list of planes taking off...")
            json_data = msg.body
            plane = jsonpickle.decode(json_data)

            # Remove aviao da lista das descolagens
            for plane in self.agent.planesTakeoff:
                if plane["id"] == str(msg.sender):
                    self.agent.planesTakeoff.remove(plane)
                    print(f"Control tower removed plane {msg.sender} from the planes taking off list.")

            


            
