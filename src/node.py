from position import Position

INFECTION = 1
ROAD_CONNECTING = 2

class Node:
    def __init__(self, id : int, type : int, position : Position):
        self.id = id
        self.type = type
        self.position = position

    def getType(self):
        return self.type

    def getPosition(self):
        return self.position
