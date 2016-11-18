# Based on the Athens course at Telecom ParisTech by Jean-Louis Dessales

import math
import Tkinter
from time import sleep
import random
from PIL import *
import PIL  # to interface Python Imaging Library with Tkinter
from Simulation import *
from Simulation_Control import *
from Draw_Area import *
from Generic_Main_Frame import *
from Ground import *


class LandCell(object):
    # defines one cell
    def __init__(self, N=0, NP=0, PP=0):
        self.Node = N
        self.PPheromone = PP  # Attractive Pheromone
        self.fieldIndex = -1

    def __add__(self, Other):
        return LandCell(self.Node + Other.Node, self.PPheromone + Other.PPheromone)


class Node(object):
    def __init__(self, x=0, y=0, iden=0):
        self.Id = iden
        self.Position = [x, y]

    def setPosition(self, Pos):
        self.Position = Pos


class Landscape(object):
    """ A 2-D grid with cells that contains pheromone or edges (for graphics)
        Graph is represented by Nodes and Edges
    """

    def __init__(self, Size):
        self.Size = Size
        self.Ground = [[LandCell() for x in range(Size)] for x in range(Size)]

        # coordinates of edges with pheromons to be drawn on the map
        # this field is update in the vaporate function
        self.EdgesWithPheromons = [];

        # represents edges - value of pheromone on each edge
        self.Edges = [[0 for col in range(NbNodes)] for row in range(NbNodes)]

        # distances between nodes
        self.Distances = [[0 for col in range(NbNodes)] for row in range(NbNodes)]

        # used to store the actual optimal path
        self.OptimalPath = 10000000000

        # create the nodes
        self.Nodes = []
        self.Nodes.append(Node(100, 260, 0))
        self.Nodes.append(Node(150, 100, 1))
        self.Nodes.append(Node(200, 120, 2))
        self.Nodes.append(Node(30, 200, 3))
        self.Nodes.append(Node(225, 123, 4))
        self.Nodes.append(Node(250, 250, 5))

        self.Nodes.append(Node(124, 90, 6))
        self.Nodes.append(Node(50, 221, 7))
        self.Nodes.append(Node(152, 152, 8))
        self.Nodes.append(Node(80, 80, 9))
        self.Nodes.append(Node(210, 85, 10))

        # compute the distances of all nodes
        for ident in range(NbNodes):
            node = self.Nodes[ident]
            for prev in range(ident):
                Direction = (complex(node.Position[0], node.Position[1]) - complex(self.Nodes[prev].Position[0],
                                                                                   self.Nodes[prev].Position[1]))
                Distance = abs(Direction)
                self.Distances[ident][prev] = Distance
                self.Distances[prev][ident] = Distance

            # Positioning the nodes  of the graph randomly
            # for ident in range(NbNodes):
            #    #symetrical
            #    position = (100+50*(ident%3),100+50*(ident/3))
            #    #random
            #    #position = (random.randint(20,Size-20),random.randint(20,Size-20))
            #    node = Node(position[0],position[1],ident)
            #    self.Nodes.append(node)
            #    Observer.record(('Node',position))
            #    for prev in range(ident):
            #        Direction = (node.Position - self.Nodes[prev].Position)
            #        Distance = abs(Direction)
            #        self.Distances[ident][prev] = Distance
            #        self.Distances[prev][ident] = Distance
            #
            #    #make the nodes big
            #    for Pos in self.neighbours(position, Radius=2):
            #        Observer.record(('Node',Pos))
            #        self.node(Pos,10)

    def evaporate(self):
        Land.EdgesWithPheromons = []
        for i in range(NbNodes):
            for j in range(NbNodes):
                # this is the value of the pheromone on the node
                cell = Land.Edges[i][j]

                cell = (1 - theta) * cell
                Land.Edges[i][j] = cell

                # if the value is higher than the limit - show the pheromone on the screen
                if cell > PToShow:
                    Land.EdgesWithPheromons.append([Land.Nodes[i].Position, Land.Nodes[j].Position])


class Ant(object):
    """ Defines individual agents - one concrete Ant. The behaviour of ant can be expressed as a state machine with the state:
        searchNextNode (search for the next node), ReturnToFirstNode, GoToNode (just go to the selected node).
    """

    def __init__(self, IdNb):
        self.IdNb = IdNb  # Identity number
        self.Action = 'SearchNextNode'
        self.Node = Node()
        self.Path = []
        self.PathLength = 0
        self.NodeDistance = -1
        self.PrevNodeIndex = -1
        self.ToVisit = []
        self.Visited = []  # empty array of visited nodes

        for i in range(NbNodes):
            self.Visited.append(0)
            self.ToVisit.append(i)

    def isCompleted(self):
        for i in range(NbNodes):
            if self.Visited[i] == 0:
                return 0

        return 1

    def goToNode(self):
        self.Visited[self.Node.Id] = 1
        self.Path.append(self.Node.Id)

        # add the distance of the node to which I just arrived
        self.PathLength += self.NodeDistance

        # if we have all nodes visited go to the first node
        if self.isCompleted():
            self.Action = 'GoToFirst'
            firstNode = self.Path[0]
            # also add the value to the length of the path
            self.PathLength += Land.Distances[self.Node.Id][firstNode]
            self.Node = Land.Nodes[self.Path[0]]

        else:
            self.Action = 'SearchNextNode'

    def goToFirst(self):
        # add the node just to make the path complete
        self.Path.append(self.Node.Id)

        # precompute the pheromone value
        self.PheromoneValue = 1 / math.pow(self.PathLength, k)

        # add the distance of the last node
        if self.PathLength < Land.OptimalPath:
            print self.Path
            print self.PathLength
            Land.OptimalPath = self.PathLength
        # remove the last added
        self.Path.pop()

        # start copying the path home
        self.Action = 'ReturnToStart'
        to = self.Path.pop()
        Land.Edges[self.Node.Id][to] += self.PheromoneValue
        Land.Edges[to][self.Node.Id] += self.PheromoneValue
        self.Node = Land.Nodes[to]

    def searchNextNode(self):
        nodeindex = self.Node.Id
        # the maximal probability
        pMax = 0
        p = 0

        # Try to select the best node by the pheromones in the direction
        # have to iterate over all nodes
        for i in range(NbNodes):
            if i != self.Node.Id and self.Visited[i] == 0:
                d = Land.Distances[self.Node.Id][i]

                # get the value of pheromon on the edge
                pi = Land.Edges[self.Node.Id][i]

                # To prevent division by zero and get some info
                # when d = 0 there would be problem in computation of d
                if d == 0:
                    print i
                    print self.Node.Id

                # the quality of the route
                nij = 1 / d

                pselected = math.pow(pi, alfa) * math.pow(nij, beta)

                # normalization
                # compute the sum of other options
                sum = 0
                for j in range(NbNodes):
                    if j != self.Node.Id and self.Visited[j] == 0 and j != i:
                        dj = Land.Distances[self.Node.Id][j]
                        pij = Land.Edges[self.Node.Id][j]
                        nj = 1 / dj
                        pj = math.pow(pij, alfa) * math.pow(nj, beta)
                        sum += pj
                if sum > 0:
                    p = pselected / sum

                # if we have a new best path - then remember the index
                if p > pMax:
                    pMax = p
                    nodeindex = i

                # for the first time when - just choose whatever node
        while nodeindex == self.Node.Id:
            nodeindex = random.randint(0, NbNodes - 1)

        # we have a new node - we will add distance
        self.PathLength += Land.Distances[self.Node.Id][nodeindex]
        self.Node = Land.Nodes[nodeindex]
        self.Action = 'GoToNode'

    def returnToStart(self):
        self.Visited[self.Node.Id] = 0

        if len(self.Path):
            to = self.Path.pop()
            # put the pheromon on the edge
            Land.Edges[self.Node.Id][to] += self.PheromoneValue
            Land.Edges[to][self.Node.Id] += self.PheromoneValue

            # change my position
            self.Node = Land.Nodes[to]

        else:
            # arrived home after the journey
            self.Action = "SearchNextNode"
            # set the precomputed value to 0
            self.PheromoneValue = 0;
            for i in range(NbNodes):
                self.ToVisit.append(i)
            self.PathLength = 0

    def moves(self):
        # here is the ants move - one of the following actions is always selected
        if self.Action == 'GoToNode':
            self.goToNode()
        if self.Action == 'SearchNextNode':
            self.searchNextNode()
        if self.Action == 'ReturnToStart':
            self.returnToStart()
        if self.Action == "GoToFirst":
            self.goToFirst()


class Ant_Frame(Generic_Main_Frame):
    def __init__(self, Parent, NbAgents):
        # frame with some additional ant capabilities
        Generic_Main_Frame.__init__(self, Parent, self.oneStep, Wtitle='Ants')
        self.startGround()
        self.LastTimeStep = 0
        self.Counter = 0
        # create population of agents
        self.Pop = [Ant('A%d' % IdNb) for IdNb in range(NbAgents)]
        self.PopSize = NbAgents
        self.Moves = 0  # counts the number of times agents have moved
        t = Thread(target=self.redraw)
        t.start()

    def startGround(self):
        """ the ground is a 2-D space representing the field where ants wander
        """
        self.Ground = Ground(self, Toric=True)
        self.Ground.scaleX = self.Ground.scaleY = LandSize  # Logical coordinates
        self.Ground.W = self.Ground.H = LandWindowSize  # Physical coordinates
        self.Ground.configure(width=self.Ground.W, height=self.Ground.H)
        self.Ground.pack(expand=Tkinter.YES, fill=Tkinter.BOTH)  # the window shows on the scren

    def oneStep(self):
        # this function is called back after each simulation step
        Land.evaporate()

        for agent in self.Pop:
            agent.moves()

        self.Moves += 1
        return 0

    def redraw(self):
        while 1:
            # the landscape is entirely redrawn
            self.Ground.erase()  # supposedly destroys all objects on ground

            self.displayNodes(Land.Nodes)
            self.displayPheromons(Land.EdgesWithPheromons)
            sleep(1)

    def displayPheromons(self, edges):
        for edge in edges:
            coord1 = edge[0]
            coord2 = edge[1]
            self.Ground.create_line(coord1[0], coord1[1], coord2[0], coord2[1], fill="red", dash=(4, 4))

    def displayNodes(self, Nodes):
        for node in Nodes:
            coord = node.Position
            self.Ground.create_rectangle(coord[0] - 2, coord[1] - 2, coord[0] + 2, coord[1] + 2, outline='black',
                                         fill='gray50')


def Start():
    MainWindow = Tkinter.Tk()  # creates the main window
    MainWindow.title('Ants')
    MainWindow.GParent = MainWindow

    Frame = Ant_Frame(MainWindow, 80)

    # displaying the window
    MainWindow.lift()
    MainWindow.focus_force()
    # Entering main loop
    MainWindow.mainloop()  # control is given to the window system
    OptimalPath = 10000000000


if __name__ == "__main__":
    LandSize = 300
    NbNodes = 11

    # level of pheromone to show
    PToShow = 0.004

    # factor which lowers the value given to a path on function of the paths length
    k = 1

    # evaporation factor
    theta = 0.07

    # parameter which amplifies the value of the pheromon on the edge (pi^alfa)
    alfa = 4

    # parameter which amplifies the impact of the quality of the route  ni^beta; ni=1/de
    beta = 2.5

    Land = Landscape(LandSize)
    LandWindowSize = 700
    Start()