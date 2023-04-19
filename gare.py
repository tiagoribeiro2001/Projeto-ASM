from spade import agent
import random

class Gare(agent.Agent):

    def __init__(self, posX, posY, isFree, type):
        super().__init__()
        self.posX = posX
        self.posY = posY
        self.free = isFree
        self.type = type