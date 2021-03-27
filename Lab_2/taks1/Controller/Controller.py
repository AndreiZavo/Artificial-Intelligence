from queue import PriorityQueue

from Domain.Node import Node


def add_to_to_search(to_search, neighbour):
    for node in to_search:
        if neighbour == node and neighbour.f >= node.f:
            return False
    return True


def add_to_search_queue(to_search, neighbour):
    for node in iter(to_search.get, None):
        if neighbour == node and neighbour.f >= node.f:
            return False
    return True


def out_of_matrix(next_node):
    if next_node[0] < 0 or next_node[0] > 19 or next_node[1] < 0 or next_node[1] > 19:
        return True
    return False


class Controller:

    def __init__(self, m, d):
        self.d = d
        self.m = m

    def a_star_search(self, initial_x, initial_y, final_x, final_y):
        to_search = []
        searched = []
        start_position = (initial_x, initial_y)
        end_position = (final_x, final_y)

        start_node = Node(start_position, None)
        end_node = Node(end_position, None)

        to_search.append(start_node)

        while len(to_search) > 0:
            to_search.sort()
            current_node = to_search.pop(0)
            searched.append(current_node)

            if current_node == end_node:
                path = []
                while current_node != start_node:
                    path.append(current_node.position)
                    current_node = current_node.parent

                return path[::-1]

            (x, y) = current_node.position

            neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for next_node in neighbours:

                if out_of_matrix(next_node) or self.m.surface[next_node[0], next_node[1]] == 1:
                    continue

                neighbour = Node(next_node, current_node)
                if neighbour in searched:
                    continue

                neighbour.set_heuristics(start_node, end_node)

                if add_to_to_search(to_search, neighbour):
                    to_search.append(neighbour)

        return None

    def greedy_search(self, initial_x, initial_y, final_x, final_y):

        queue = PriorityQueue()
        queue.put((0, (initial_x, initial_y)))
        added = [(initial_x, initial_y)]

        previous = {}

        for i in range(0, 21):
            previous[i] = []
            for j in range(0, 21):
                previous[i].append((-1, -1))

        while not queue.empty():
            poz = queue.get()
            x = poz[1][0]
            y = poz[1][1]

            if (x, y) == (final_x, final_y):
                break

            if x > 0:
                if self.m.surface[x - 1][y] != 1 and (x - 1, y) not in added:
                    queue.put((abs(x - 1 - final_x) + abs(y - final_y),
                               (x - 1, y)))
                    added.append((x - 1, y))
                    previous[x - 1][y] = (x, y)
            if x < 19:
                if self.m.surface[x + 1][y] != 1 and (x + 1, y) not in added:
                    queue.put((abs(x + 1 - final_x) + abs(y - final_y), (x + 1, y)))
                    added.append((x + 1, y))
                    previous[x + 1][y] = (x, y)
            if y > 0:
                if self.m.surface[x][y - 1] != 1 and (x, y - 1) not in added:
                    queue.put((abs(x - final_x) + abs(y - 1 - final_y), (x, y - 1)))
                    added.append((x, y - 1))
                    previous[x][y - 1] = (x, y)
            if y < 19:
                if self.m.surface[x][y + 1] != 1 and (x, y + 1) not in added:
                    queue.put((abs(x - final_x) + abs(y + 1 - final_y), (x, y + 1)))

                    added.append((x, y + 1))
                    previous[x][y + 1] = (x, y)

        path = []
        if previous[final_x][final_y] == (-1, -1):
            return path
        path.append((final_x, final_y))
        poz = path[0]
        while poz != (initial_x, initial_y):
            path.insert(0, previous[poz[0]][poz[1]])
            poz = path[0]

        return path


