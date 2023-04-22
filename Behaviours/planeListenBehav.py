from spade.behaviour import CyclicBehaviour
from spade.message import Message
from dados import XMPP_SERVER
import jsonpickle
import time

class PlaneListenBehav(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=1000)
        toDo = msg.get_metadata("performative")
        print(f"Plane received: {toDo}")

        # Aterragem autorizada 
        if toDo == "landing_authorized":
            json_data = msg.body
            mensagem = jsonpickle.decode(json_data)
            self.agent.runway = mensagem["runway"]
            self.agent.gare = mensagem["gare"]

            # Espera o tempo que demora a aterrar
            print(f"Plane {str(self.agent.jid)} starting the landing")
            time.sleep(self.agent.landingTime)
            
            # Espera o tempo que fica na pista
            print(f"Plane {str(self.agent.jid)} has landed in runway {str(self.agent.runway)}")
            self.agent.state = "ground"
            time.sleep(self.agent.runwayTime)

            # Envia mensagem à torre de controlo para desocupar a pista
            response = Message(to="tower@" + XMPP_SERVER)
            response.set_metadata("performative", "free_runway")
            json_data = jsonpickle.encode(self.agent.runway)
            response.body = json_data
            print(f"Plane {str(self.agent.jid)} indicating control tower that the runway {str(self.agent.runway)} is free...")
            await self.send(response)


            # Espera o tempo de viagem desde a pista ate a gare
            print(f"Plane {str(self.agent.jid)} going from runway {str(self.agent.runway)} to gare {str(self.agent.gare)}.")
            time.sleep(self.agent.moveTime)

            # Altera o estado do aviao para parkado
            print(f"Plane {str(self.agent.jid)} reached gare {str(self.agent.gare)}. The plane is now parked.")
            self.agent.state = "parked"

        # Aterragem nao autorizada
        elif toDo == "landing_not_authorized":
            pass
    
        # Descolagem autorizada
        elif toDo == "takeoff_authorized":
            json_data = msg.body
            runway = jsonpickle.decode(json_data)

            # Altera a pista e o estado do aviao
            self.agent.runway = runway
            self.agent.state = "ground"

            # Aviao a ir da gare para a pista
            print(f"Plane {str(self.agent.jid)} going from gare {str(self.agent.gare)} to runway {str(self.agent.runway)}.")
            self.agent.gare = None
            time.sleep(self.agent.moveTime)

            # Espera o tempo que fica na pista
            print(f"Plane {str(self.agent.jid)} is taking off in runway {str(self.agent.runway)}")
            time.sleep(self.agent.runwayTime)

            # Envia mensagem à torre de controlo para desocupar a pista
            response = Message(to="tower@" + XMPP_SERVER)
            response.set_metadata("performative", "free_runway")
            json_data = jsonpickle.encode(self.agent.runway)
            response.body = json_data
            await self.send(response)
            print(f"Plane {str(self.agent.jid)} took off. Indicating control tower that the runway {str(self.agent.runway)} is free...")
            
            
            
            self.agent.state = "air"

            await self.agent.stop()
            print(f"Plane {str(self.agent.jid)} has left the airport.")


        # Descolagem nao autorizada
        elif toDo == "takeoff_not_authorized":
            pass