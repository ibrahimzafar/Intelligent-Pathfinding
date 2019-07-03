import heapq
from path_finding import PathFinding, distance
from random import randint

class A_Star(PathFinding):
    def __init__(self):
        self.open_list = []
        heapq.heapify(self.open_list)
        self.closed = set()
        self.patients = None
        PathFinding.__init__(self)
        self.init_grid()
    #checks if the specific node is inside the grid
    def in_grid(self, r, c):
        if 0 < c < self.grid_cols and 0 < r < self.grid_rows:
            return True
        return False
    #returns the neighbouring 8 nodes of any node, like so
            # # #
            # X #
            # # #
    def get_neighbours(self, current):
        valid_indices = [(current.r + i, current.c + j) for i in range(-1, 2, 1) for j in range(-1, 2, 1) if
                         0 <= current.r + i < self.grid_rows and 0 <= current.c + j < self.grid_cols]
        neighbours = [self.get(i, j) for (i, j) in valid_indices]
        neighbours.remove(current)
        neighbours = [n for n in neighbours if n is not None]
        return neighbours
    #this function saves the path of traversed nodes by backtracking up to the start node
    def make_path(self, node, start):
        path = []
        while node is not start:
            path.append(node)
            if node.parent is None:
                break
            node = node.parent
            if node.parent == node:
                break
        path.append(start)
        return path
    #optimal route planning algorithm for an ambulance, that has to pick up N patients
    def rescue_patients(self, total):
        self.add_patients(total)
        path = []
        count = 0
        patients = self.patients[:]
        current = self.start
        while True:
            if count == total:
                break
            add_path, current = self.A_star_algorithm_multiple_goals(current, patients)
            path.extend(add_path[::-1])
            count += 1
        self.plot_path(path)
    #this function performs A* search betweeen one starting position, and one ending position
    def A_star_algorithm(self):
        path=[]
        self.start.update(self.start, self.goal)
        heapq.heappush(self.open_list, (self.start.f, self.start))
        while (len(self.open_list) > 0):
            f, current = heapq.heappop(self.open_list)
            self.closed.add(current)

            if current == self.goal:
                path = self.make_path(current, self.start)
                break
            neighbours = self.get_neighbours(current)
            for neighbour in neighbours:
                if neighbour.reachable and neighbour not in self.closed:
                    if (neighbour.f, neighbour) in self.open_list:
                        if neighbour.g > current.g + distance(current, neighbour):
                            neighbour.update(current, self.goal)
                    else:
                        neighbour.update(current, self.goal)
                        heapq.heappush(self.open_list, (neighbour.f, neighbour))
        self.plot_path(path)
    #Note that this implementation with multiple goals and a single start node
    #may be slightly different from the classical algorithm A* which takes into account
    #current cost, and heuristic cost => F(n) = G(n) + H(n)
    #Here, at every step, heuristic estimates for ALL the goal states(patients) is estimated, and a
    #step is taken towards the goal state with minimum distance
    def A_star_algorithm_multiple_goals(self, start, goals):
        path=[]
        current=[]
        start.update_all_f(start, goals)
        self.open_list.clear()
        self.closed.clear()
        heapq.heappush(self.open_list, (start.f, start))
        while (len(self.open_list) > 0):
            f, current = heapq.heappop(self.open_list)
            self.closed.add(current)
            if current in goals:
                path = self.make_path(current, start)
                goals.remove(current)
                print('Patients remaining:',len(goals))
                break
            neighbours = self.get_neighbours(current)
            for neighbour in neighbours:
                if neighbour.reachable and neighbour not in self.closed:
                    #                    if current is not neighbour:
                    if (neighbour.f, neighbour) in self.open_list:
                        if neighbour.g > current.g + distance(current, neighbour):
                            neighbour.update_all_f(current, goals)
                    else:
                        neighbour.update_all_f(current, goals)
                        heapq.heappush(self.open_list, (neighbour.f, neighbour))
        return path, current


A = A_Star()
#this function is called for a single patient
#A.A_star_algorithm()

#30 patients are being rescued at a time
A.rescue_patients(30)
