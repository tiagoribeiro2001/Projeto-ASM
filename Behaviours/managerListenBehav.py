from spade.behaviour import CyclicBehaviour
from spade.message import Message

class ManagerListenBehaviour(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=10)
        if msg:
            # Processar a mensagem da torre de controle e atualizar a informação
            # Verificar o tipo de mensagem (aterrissagem, decolagem, etc.) e atualizar a lista de aviões (self.agent.avioes)
            # Implementação de lógica para adicionar aviões às filas de aterragem e descolagem com base nas regras fornecidas
            pass
        else:
            print("ManagerAgent: Nenhuma mensagem recebida.")
