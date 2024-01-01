from position import Position

class Node:
    def __init__(self, id : int, position : Position):
        self.id = id
        self.position = position

    def getType(self):
        return self.type

    def getPosition(self):
        return self.position
