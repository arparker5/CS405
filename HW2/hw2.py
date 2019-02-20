
import math

class Node:
    __nodecoord = ()            # Needs to know neighbors, distance from end, distance to all neighbors
    __distend = 0
    __cost = 0
    __weight = 0                  # Cost to Node + Distance to the end point
    __previousnode = 0
    __visited = 0               # 0 = not visited, 1 = visited

    def __init__(self, coord, endcoord, prevnode=None):
        self.__nodecoord = coord
        self.__dist = math.sqrt((endcoord[0] - self.__nodecoord[0])**2 + (endcoord[1] - self.__nodecoord[1])**2)
        if prevnode is not None:
            self.__previousnode = prevnode
            self.__cost = prevnode.getcost() + 1
            self.__weight = self.__dist + self.__cost

    def printcoord(self):
        print(self.__nodecoord[0], ",", self.__nodecoord[1])

    def getcoord(self):
        return self.__nodecoord[0], self.__nodecoord[1]

    def getx(self):
        return self.__nodecoord[0]

    def gety(self):
        return self.__nodecoord[1]

    '''def setweight(self, previouscost):
        self.__weight = self.__dist + previouscost + 1'''

    def getweight(self):
        return self.__weight

    def getdist(self):
        return self.__dist

    '''def setprevious(self, prevnode):
        self.__previousnode = prevnode.copy()'''

    def getcost(self):
        return self.__cost

    def getprevcoord(self):
        try:
            return self.__previousnode.getcoord()
        except AttributeError:
            return 0, 0

    def isvisited(self):
        return self.__visited


class BinaryHeap:   # Code for binary heap is based off of code found on interactivepython.org
    def __init__(self, nodelist):
        self.__heapsize = 0
        self.__heaplist = nodelist.copy()

    def moveup(self, x):
        while x // 2 > 0:
            if self.__heaplist[x].getweight() < self.__heaplist[x // 2].getweight():
                temp = self.__heaplist[x // 2]
                self.__heaplist[x // 2] = self.__heaplist[x]
                self.__heaplist[x] = temp
            x = x // 2

    def insert(self, i):
        self.__heaplist.append(i)
        self.__heapsize += 1
        self.moveup(self.__heapsize)

    def movedown(self, y):
        while(y * 2) <= self.__heapsize:
            mc = self.minChild(y)
            if self.__heaplist[y].getweight() > self.__heaplist[mc].getweight():
                temp = self.__heaplist[y]
                self.__heaplist[y] = self.__heaplist[mc]
                self.__heaplist[mc] = temp
            y = mc

    def minChild(self, i):
        if i * 2 + 1 > self.__heapsize:
            return i * 2
        else:
            if self.__heaplist[i * 2].getweight() < self.__heaplist[i*2+1].getweight():
                return i * 2
            else:
                return i * 2 + 1

    def makeHeap(self, newheap):
        i = len(newheap) // 2
        self.__heapsize = len(newheap)
        self.__heaplist = [0] + newheap[:]
        while i > 0:
            self.movedown(i)
            i = i-1

    def popmin(self):
        ret = self.__heaplist[1].getweight()
        self.__heaplist[1] = self.__heaplist[self.__heapsize]
        self.__heapsize -= 1
        self.__heaplist.pop()
        self.movedown(1)
        return ret

    def printheap(self):
        for i in range(1, len(self.__heaplist)):
            print(self.__heaplist[i].getweight())


class Environment:                # Needs to print maze, needs 2D array of [coordinates : Node]

    __startcoord = ()
    __endcoord = ()
    __nodes = []

    nodecount = 0

    __line = []                 # Array of strings, represents each line of the board

    __line.append("#################")
    __line.append("#S....#.........#")
    __line.append("#.###.#.#####.#.#")
    __line.append("#.#.#.#...#...#.#")
    __line.append("#.#.#.#####.###.#")
    __line.append("#.#.....#...#.#.#")
    __line.append("#.#####.#.###.#.#")
    __line.append("#.....#...#....E#")
    __line.append("#################")

    def printmazestart(self):
        for i in range(len(self.__line)):
            print(self.__line[i])

    def genstartend(self):                    # Finds all "." on the maze and makes a Node object with their coordinate
        for i in range(1, len(self.__line) - 1): # Finds start and end of the maze
            for j in range(1, len(self.__line[0]) - 1):
                if self.__line[i][j] == "S":
                    self.__startcoord = (j, i)
                    print(self.__startcoord[0], ",", self.__startcoord[1], " START")
                elif self.__line[i][j] == "E":
                    self.__endcoord = (j, i)
                    print(self.__endcoord[0], ",", self.__endcoord[1], " END")

        '''for i in range(1, len(self.__line) - 1):     #Finds all "." on the maze and makes the Node objects
            for j in range(1, len(self.__line[0]) - 1):
                if self.__line[i][j] == ".":
                    self.__nodes.append(Node((j, i), self.__endcoord))'''

        for i in self.__nodes:
            i.printcoord()

    def checkaround(self, node):  # Takes a node, returns a list of all neighboring nodes that are not the previous node
        hlist = []
        if node.getcoord() != node.getprevcoord() and self.__line[node.gety() - 1][node.getx()] == ".":
            hlist.append(Node((node.getx(), node.gety() - 1), self.__endcoord, node))
        if node.getcoord() != node.getprevcoord() and self.__line[node.gety()][node.getx() + 1] == ".":
            hlist.append(Node((node.getx() + 1, node.gety()), self.__endcoord, node))
        if node.getcoord() != node.getprevcoord() and self.__line[node.gety() + 1][node.getx()] == ".":
            hlist.append(Node((node.getx(), node.gety() + 1), self.__endcoord, node))
        if node.getcoord() != node.getprevcoord() and self.__line[node.gety()][node.getx() - 1] == ".":
            hlist.append(Node((node.getx() - 1, node.gety()), self.__endcoord, node))
        return hlist

    def mazesearch(self):
        s = Node(self.__startcoord, self.__endcoord)
        heap = BinaryHeap([])
        newlist = E1.checkaround(s)
        for i in newlist:
            print(i.getcoord(), ", weight:", i.getweight(), ", cost:", i.getcost(), ", dist:", i.getdist())



E1 = Environment()
E1.printmazestart()
E1.genstartend()
E1.mazesearch()
