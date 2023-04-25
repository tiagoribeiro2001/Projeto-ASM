from spade.behaviour import CyclicBehaviour
from spade.message import Message
from dados import XMPP_SERVER

class ManagerListenBehaviour(CyclicBehaviour):

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




            # Processar a mensagem da torre de controle e atualizar a informação

            # Verificar o tipo de mensagem (aterrissagem, decolagem, etc.) e atualizar a lista de aviões (self.agent.avioes)
            # Implementação de lógica para adicionar aviões às filas de aterragem e descolagem com base nas regras fornecidas
            pass
        else:
            print("ManagerAgent: Nenhuma mensagem recebida.")
