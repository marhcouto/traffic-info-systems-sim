
def max_num_vehicles():
    return int(350 / 20)


def roads():
    roads = []
    r1 = ["A", "B", 150, 16, False]
    r2 = ["A", "C", 50, 7, False]
    r3 = ["A", "D", 150, 16, False]
    r4 = ["B", "C", 50, 12, False]
    r5 = ["B", "E", 100, 14, False]
    r7 = ["C", "J", 50, 10, False]
    r8 = ["E", "J", 50, 10, False]
    r9 = ["E", "H", 50, 5, False]
    r10 = ["H", "J", 50, 10, False]
    r11 = ["D", "F", 150, 5, False]
    r12 = ["F", "G", 150, 10, False]
    r13 = ["G", "J", 200, 10, False]
    r14 = ["C", "I", 50, 5, False]
    r15 = ["I", "G", 50, 5, False]

    roads.append(r1)
    roads.append(r2)
    roads.append(r3)
    roads.append(r4)
    roads.append(r5)
    roads.append(r7)
    roads.append(r8)
    roads.append(r9)
    roads.append(r10)
    roads.append(r11)
    roads.append(r12)
    roads.append(r13)
    roads.append(r14)
    roads.append(r15)

    return roads

def nodes():
    nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    return nodes

def start_node():
    return "A"

def end_node():
    return "J"

