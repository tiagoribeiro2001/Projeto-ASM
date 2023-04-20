from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from dados import XMPP_SERVER

class LandingRequestBehav(OneShotBehaviour):
        async def run(self):
            # cria a mensagem com as informações do voo
            msg = Message(to="tower@" + XMPP_SERVER)  # destinatário é a torre de controle
            msg.body = f"{str(self.agent.jid)}|{self.agent.company}|{self.agent.type}|{self.agent.origin}|{self.agent.destiny}"
            print("Plane requesting to land")
            
            # envia a mensagem
            await self.send(msg)