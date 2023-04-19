from plane import PlaneAgent
from tower import TowerAgent
import time
from dados import XMPP_SERVER, PASSWORD

if __name__ == "__main__":

    tower = TowerAgent ("tower@" + XMPP_SERVER, PASSWORD)
    
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