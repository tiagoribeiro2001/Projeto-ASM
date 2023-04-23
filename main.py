from plane import PlaneAgent
from tower import TowerAgent
from gare import GareAgent
from manager import ManagerAgent
import time
from dados import XMPP_SERVER, PASSWORD

if __name__ == "__main__":

    tower = TowerAgent("tower@" + XMPP_SERVER, PASSWORD)
    gare = GareAgent("gare@" + XMPP_SERVER, PASSWORD)
    manager = ManagerAgent("manager@" + XMPP_SERVER, PASSWORD)
    plane = PlaneAgent("plane1@" + XMPP_SERVER, PASSWORD)

    
    future = gare.start()
    future.wait()

    future = tower.start()
    future.wait()

    future = manager.start()
    future.wait()

    future = plane.start()
    future.wait()

    
    while plane.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            tower.stop()
            plane.stop()
            gare.stop()
            manager.stop()
            break

    '''
    future = manager.start()
    future.wait()

    future = taxi.start()
    future.wait()

    future = customer.start()
    future.wait()

    while customer.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            manager.stop()
            taxi.stop()
            customer.stop()
            break
    
    '''
    print("Agents finished")