def max_num_vehicles():
    return int(350 / 20)


def roads():
    roads = []
    r1 = ["A", "C", 200, 20]
    r2 = ["A", "B", 150, 16]
    r3 = ["B", "D", 150, 4]
    r4 = ["C", "D", 250, 10]
    roads.append(r1)
    roads.append(r2)
    roads.append(r3)
    roads.append(r4)
    return roads


def nodes():
    nodes = ["A", "B", "C", "D"]
    return nodes


def start_node():
    return "A"


def end_node():
    return "D"
