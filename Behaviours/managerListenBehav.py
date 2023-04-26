from spade.behaviour import CyclicBehaviour
from spade.message import Message
from dados import XMPP_SERVER
import jsonpickle

class ManagerListenBehaviour(CyclicBehaviour):

    def __init__(self, period, **kwargs):
        super().__init__(period, **kwargs)

    async def run(self):
        
        # Cria a mensagem com as informacoes do voo
        msg = Message(to="tower@" + XMPP_SERVER)  # destinatário é a torre de controle
        msg.set_metadata("performative", "inform")
        msg.body = "Nada"
        print(f"Asking information to tower...")

        # Recebe a mensagem
        message = await self.receive(timeout=1000)
        toDo = message.get_metadata("performative")

        if toDo:
            data = jsonpickle.decode(toDo.body)
            if data["action"] == "update_info":
                self.agent.landingQueue = data["landingQueue"]
                self.agent.takeoffQueue = data["takeoffQueue"]
                self.agent.planesLanding = data["planesLanding"]
                self.agent.planesTakeoff = data["planesTakeoff"]
                self.display_info()
        else:
            print("ManagerAgent: Nenhuma mensagem recebida.")
        

    def display_info(self):
        print("------------------ Airport Information ------------------")
        print("Landing Queue: ", self.agent.list1)
        print("Takeoff Queue: ", self.agent.list2)
        print("Planes Landing: ", self.agent.list3)
        print("Planes Takeoff: ", self.agent.list4)
        print("---------------------------------------------------------")