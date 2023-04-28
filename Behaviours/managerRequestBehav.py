from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from dados import XMPP_SERVER
import jsonpickle

class ManagerRequestBehav(PeriodicBehaviour):

    async def run(self):
        
        # Cria a mensagem com as informacoes do voo
        msg = Message(to="tower@" + XMPP_SERVER)  # destinatário é a torre de controle
        msg.set_metadata("performative", "request_information")
        print(f"Manager asking control tower for information...")
        await self.send(msg)

        # Recebe a mensagem
        message = await self.receive(timeout=1000)
        toDo = message.get_metadata("performative")

        if toDo == "response_information":

            data = jsonpickle.decode(message.body)
            self.agent.landingQueue = data["landingQueue"]
            self.agent.takeoffQueue = data["takeoffQueue"]
            self.agent.planesLanding = data["planesLanding"]
            self.agent.planesTakeoff = data["planesTakeoff"]
            self.display_info()
        else:
            print("ManagerAgent: Nenhuma mensagem recebida.")
        

    def display_info(self):
        print("------------------ Airport Information ------------------")
        print("Landing queue: ", self.agent.landingQueue)
        print("Takeoff queue: ", self.agent.takeoffQueue)
        print("Planes landing: ", self.agent.planesLanding)
        print("Planes taking off: ", self.agent.planesTakeoff)
        print("---------------------------------------------------------")