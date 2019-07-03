from math import sqrt
from random import randint
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import os

class Node:
    def __init__(self, r, c, reachable):
        self.r = r
        self.c = c
        self.g = 0
        self.h = 0
        self.f = 0
        self.all_h = []
        self.all_f = []
        self.parent = None
        self.reachable = reachable
    #cost for all goal states/patients is estimated
    def update_all_f(self, parent, goals):
        self.all_h = [0] * len(goals)
        self.all_f = [0] * len(goals)
        self.g = parent.g + distance(self, parent)
        for i in range(0, len(goals)):
            self.all_h[i] = distance(self, goals[i])
            self.all_f[i] = self.g + self.all_h[i]
            if len(goals) == 1:
                self.f = self.all_f[0]
            else:
                self.f = min(self.all_f)
        self.parent = parent

    # cost for single goal state/patient is estimated
    def update(self, parent, goal_state):
        self.g = parent.g + distance(self, parent)
        self.h = distance(self, goal_state)
        self.f = self.g + self.h
        self.parent = parent
    def __lt__(self, other):
        return self.f < other.f

#this is the super class which we will inherit in a pathfinding problem
#using Genetic Algorithm and Algorithm A*.
class PathFinding:
    def __init__(self):
        self.grid=[]
    def get(self, r, c):
        try:
            return self.grid[r * self.grid_cols + c]
        except:
            print(r, c)
            print(r * self.grid_cols + c)
    #initialization of grid, and blocked nodes
    def init_grid(self, width=200, height=200):
        self.grid_cols = width
        self.grid_rows = height
        #blocked Nodes in the grid accounts for 0.5% of the total area
        self.walls = [(randint(0, self.grid_rows), randint(0, self.grid_cols)) for i in range(0, int(0.005*(width*height)))]
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                if (r, c) in self.walls:
                    reachable = False
                else:
                    reachable = True
                self.grid.append(Node(r, c, reachable))
        while (True):
            self.start = self.get(randint(0, self.grid_rows - 1), randint(0, self.grid_cols - 1))
            self.goal = self.get(randint(0, self.grid_rows - 1), randint(0, self.grid_cols - 1))
            if self.start.reachable and self.goal.reachable:
                break
    #grid displayed
    def display_grid(self, path):
        os.system('CLS')
        for r in range(0, self.grid_rows):
            for c in range(0, self.grid_cols):
                node = self.get(r, c)
                if node.reachable == True:
                    if node in path:
                        print('1', sep=' ', end=' ', flush=True)
                    else:
                        print('0', sep=' ', end=' ', flush=True)
                else:
                    print('X', sep=' ', end=' ', flush=True)
            print('\n', sep='', end='', flush=True)
    #path plotted
    def plot_path(self, path):
        fig, ax = plt.subplots()
        Path = mpath.Path

        path_data = []
        # path
        for i in range(0, len(path)):
            if (i == 0):
                path_data.append((Path.MOVETO, (path[i].r, path[i].c)))
            if (i == len(path) - 1):
                path_data.append((Path.CLOSEPOLY, (path[i].r, path[i].c)))
            else:
                path_data.append((Path.LINETO, (path[i].r, path[i].c)))

        codes, verts = zip(*path_data)
        path = mpath.Path(verts, codes)
        patch = mpatches.PathPatch(path, facecolor='w', alpha=0.5)

        # plot control points and connecting lines
        x, y = zip(*path.vertices)
        line, = ax.plot(x, y, 'go-')

        # walls
        walls_data = []
        for i in range(0, len(self.walls)):
            walls_data.append((Path.MOVETO, (self.walls[i][0], self.walls[i][1])))
        codes, verts = zip(*walls_data)
        walls = mpath.Path(verts, codes)
        patch = mpatches.PathPatch(walls, facecolor='w', alpha=0.5)

        x, y = zip(*walls.vertices)
        dots, = ax.plot(x, y,
                        'rx')  # go for dots , go- for line thru dots, go-- dotted line thru dots, '' for straight blue line
        # p = polygon, s = square
        # patients
        if (self.patients is not None):
            pt_data = []
            for i in range(0, len(self.patients)):
                pt_data.append((Path.MOVETO, (self.patients[i].r, self.patients[i].c)))
            codes, verts = zip(*pt_data)
            patients = mpath.Path(verts, codes)
            patch = mpatches.PathPatch(patients, facecolor='w', alpha=0.5)

            x, y = zip(*patients.vertices)
            pts, = ax.plot(x, y, 'bs')

            ax.legend((line, dots, pts), ('A*', 'Blocked', 'Patients'))

        else:
            ax.legend((line, dots), ('A*', 'Blocked'))
        ax.grid()
        ax.axis('equal')
        plt.show()
    #adds patients to the grid
    def add_patients(self, total):
        self.patients = []
        while (len(self.patients) < total):
            r = randint(0, self.grid_rows - 1)
            c = randint(0, self.grid_cols - 1)
            node = self.get(r, c)
            if node.reachable:
                self.patients.append(node)


def distance(p0, p1):
        return sqrt(((p0.r - p1.r) ** 2 + (p0.c - p1.c) ** 2))
