def roads():
    roads = []
    r1 = ["A", "C", 200, 20]
    r2 = ["A", "B", 150, 15]
    r3 = ["B", "C", 60, 4]
    roads.append(r1)
    roads.append(r2)
    roads.append(r3)
    return roads


def nodes():
    nodes = ["A", "B", "C"]
    return nodes


def start_node():
    return "A"


def end_node():
    return "C"
