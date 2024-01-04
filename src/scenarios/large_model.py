
def max_num_vehicles():
    return int(350 / 20)


def roads():
    roads = []
    r1 = [0, 1, 150, 16, False]
    r2 = [0, 2, 50, 7, False]
    r3 = [0, 3, 150, 16, False]
    r4 = [1, 2, 50, 12, False]
    r5 = [1, 4, 100, 14, False]
    r7 = [2, 9, 50, 10, False]
    r8 = [4, 9, 50, 10, False]
    r9 = [4, 7, 50, 5, False]
    r10 = [7, 9, 50, 10, False]
    r11 = [3, 5, 150, 5, False]
    r12 = [5, 6, 150, 10, False]
    r13 = [6, 9, 200, 10, False]
    r14 = [2, 8, 50, 5, False]
    r15 = [8, 6, 50, 5, False]

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
    nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    return nodes

def start_node():
    return 0

def end_node():
    return 9

