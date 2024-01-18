def roads():
    roads = []
    r1 = [0, 1, 200, 5]
    r2 = [0, 2, 100, 7]
    r3 = [0, 4, 50, 10,]
    r4 = [1, 3, 150, 10]
    r5 = [1, 4, 50, 8]
    r7 = [2, 3, 50, 10]
    r8 = [2, 5, 50, 15]
    r9 = [3, 5, 200, 5]
    r10 = [4, 5, 100, 12]

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
