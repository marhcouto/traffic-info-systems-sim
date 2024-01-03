
def max_num_vehicles():
    return int(350 / 20)
def roads():
    roads = []
    r1 = ["A", "C", 200, 20]
    r2 = ["A", "B", 150, 16]
    r3 = ["B", "C", 150, 0]
    r4 = ["C", "E", 300, 7]
    r5 = ["C", "D", 50, 5]
    r6 = ["D", "E", 50, 0]
    roads.append(r1)
    roads.append(r2)
    roads.append(r3)
    roads.append(r4)
    roads.append(r5)
    roads.append(r6)
    return roads

def nodes():
    nodes = ["A", "B", "C", "D", "E"]
    return nodes

def start_node():
    return "A"

def end_node():
    return "D"
