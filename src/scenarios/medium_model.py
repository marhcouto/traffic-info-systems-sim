
def roads():
    roads = []
    r1 = [0, 1, 200, 5, False]
    r2 = [0, 2, 100, 7, False]
    r3 = [0, 4, 50, 10, False]
    r4 = [1, 3, 150, 10, False]
    r5 = [1, 4, 50, 8, False]
    r7 = [2, 3, 50, 10, False]
    r8 = [2, 5, 50, 15, False]
    r9 = [3, 5, 200, 5, False]
    r10 = [4, 5, 100, 12, False]
    
    roads.append(r1)
    roads.append(r2)
    roads.append(r3)
    roads.append(r4)
    roads.append(r5)
    roads.append(r7)
    roads.append(r8)
    roads.append(r9)
    roads.append(r10)

    return roads

def nodes():
    nodes = range(6)
    return nodes

def start_node():
    return 0

def end_node():
    return 5
