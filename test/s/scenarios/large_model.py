# !
# \brief Returns the maximum number of vehicles that can be in the model.
# \return The maximum number of vehicles that can be in the model.
def max_num_vehicles():
    return int(350 / 20)


# !
# \brief Creates the roads for the model.
# \return A list of roads.
def roads():
    roads = []
    r1 = [0, 1, 150, 16]
    r2 = [0, 2, 50, 7]
    r3 = [0, 3, 150, 16]
    r4 = [1, 2, 50, 12]
    r5 = [1, 4, 100, 14]
    r7 = [2, 9, 50, 10]
    r8 = [4, 9, 50, 10]
    r9 = [4, 7, 50, 5]
    r10 = [7, 9, 50, 10]
    r11 = [3, 5, 150, 5]
    r12 = [5, 6, 150, 10]
    r13 = [6, 9, 200, 10]
    r14 = [2, 8, 50, 5]
    r15 = [8, 6, 50, 5]

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


# !
# \brief Creates the list of nodes ids for the model.
# \return A list of nodes ids.
def nodes():
    nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    return nodes


# !
# \brief Returns the id of the start node.
# \return The id of the start node.
def start_node():
    return 0


# !
# \brief Returns the id of the end node.
# \return The id of the end node.
def end_node():
    return 9
