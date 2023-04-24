from spade.behaviour import CyclicBehaviour
from Behaviours.gareRequestBehav import GareRequestBehav
from Behaviours.gareLocationBehav import GareLocationBehav
from Behaviours.gareAvailableBehav import GareAvailableBehav
import jsonpickle


class gareListenBehav(CyclicBehaviour):

    async def run(self):
        # Recebe a mensagem
        msg = await self.receive(timeout=1000)
        toDo = msg.get_metadata("performative")

        # Recebe pedido da torre de controlo a pedir as gares livres
        if toDo == "request_gare":
            print(f"Gare manager received: {toDo}")
            json_data = msg.body
            plane_info = jsonpickle.decode(json_data)

            a = GareRequestBehav(plane_info)
            self.agent.add_behaviour(a)


        # Recebe pedido da torre de controlo a pedir a localizacao da gare
        elif toDo == "gare_location_request":
            print(f"Gare manager received: {toDo}")
            json_data = msg.body
            plane_info = jsonpickle.decode(json_data)

            a = GareLocationBehav(plane_info)
            self.agent.add_behaviour(a)

        elif toDo == "available_gares":
            print(f"Gare manager received: {toDo}")
            json_data = msg.body
            plane_type = jsonpickle.decode(json_data)

            a = GareAvailableBehav(plane_type)
            self.agent.add_behaviour(a)