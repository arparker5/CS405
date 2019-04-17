'''
Andrew Parker
Cameron K. Titus
Curtis Fortenberry
Laura Lundell
CS 405

A* Search

Dr. Metzgar
'''
import math
import time


class Node:
	__nodecoord = ()
	__distend = 0
	__cost = 0
	__weight = 0                  # Cost to Node + Distance to the end point
	__previousnode = 0
	
	def __init__(self, coord, endcoord,hType, prevnode=None):
		self.__nodecoord = coord
		# self.__dist = math.sqrt((endcoord[0] - self.__nodecoord[0])**2 + (endcoord[1] - self.__nodecoord[1])**2)
		self.__hType = hType
		if self.__hType=='euclidean':
			self.__dist = math.sqrt((endcoord[0] - self.__nodecoord[0])**2 + (endcoord[1] - self.__nodecoord[1])**2)
		elif self.__hType=='manhattan':
			self.__dist = (abs(self.__nodecoord[0]-endcoord[0]) + abs(self.__nodecoord[1]-endcoord[1]))
		elif self.__hType=='octile':
			self.__dist = (max(abs(self.__nodecoord[0]-endcoord[0]),abs(self.__nodecoord[1]-endcoord[1])) 
						   + 
						  (math.sqrt(2)-1)*min(abs(self.__nodecoord[0]-endcoord[0]),abs(self.__nodecoord[1]-endcoord[1])))
		elif self.__hType=='chebyshev':
			self.__dist = max(abs(self.__nodecoord[0]-endcoord[0]),abs(self.__nodecoord[1]-endcoord[1]))
		if prevnode is not None:
			self.__previousnode = prevnode
			self.__cost = prevnode.getcost() + 1
			self.__weight = self.__dist + self.__cost
		sim.env.setvisited(self.__nodecoord)

	def printcoord(self):
		print(self.__nodecoord[0], ",", self.__nodecoord[1])

	def getcoord(self):
		return self.__nodecoord[0], self.__nodecoord[1]

	def getx(self):
		return self.__nodecoord[0]

	def gety(self):
		return self.__nodecoord[1]

	def getweight(self):
		return self.__weight

	def getdist(self):
		return self.__dist

	def getcost(self):
		return self.__cost

	def getprevcoord(self):
		try:
			return self.__previousnode.getcoord()
		except AttributeError:
			return 0, 0

	def getprevnode(self):
		return self.__previousnode

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
		ret = self.__heaplist[1]
		self.__heaplist[1] = self.__heaplist[self.__heapsize]
		self.__heapsize -= 1
		self.__heaplist.pop()
		self.movedown(1)
		return ret

	def printheap(self):
		for i in range(1, len(self.__heaplist)):
			print(self.__heaplist[i].getcoord())

class Agent:
	
	def __init__(self):
		self.percepts = []
		self.pathlist = []
	
	def sense(self, env):
		self.percepts.append(env.getStart())  # [0]: start coord
		self.percepts.append(env.getEnd())    # [1]: end coord
	
	def think(self, hType):
		s = Node(self.percepts[0], self.percepts[1], hType)
		heap = BinaryHeap([])
		heap.makeHeap(sim.env.checkaround(s, hType))
		while True:                                             # Main program loop. Executes the A* Search algorithm
			nextnode = heap.popmin()
			nextneighbors = sim.env.checkaround(nextnode, hType)
			if isinstance(nextneighbors, tuple):
				print("End found!")
				endnode = nextneighbors[1]
				break
			for i in nextneighbors:
				heap.insert(i)

		pathlength = 2

		while True:                                           # Walks backward through previous nodes to generate path
			if endnode.getprevcoord() == self.percepts[0]:
				break
			self.pathlist.append(endnode.getprevcoord())
			endnode = endnode.getprevnode()
			pathlength += 1
		return pathlength
	
	def act(self, env):
		env.resetmaze()
		env.drawPath(self.pathlist)                               # Maps out the final path to the end of the maze
		env.printmaze()


class Environment:
	__line = []                   # Array of strings, represents each line of the board
	__startcoord = ()
	__endcoord = ()
	__nodes = []
	__visitedlist = []
	__pathlist = []


	def resetmaze(self):
		self.__line = []		# don't comment this line out!!!


		self.__line.append(['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'])
		self.__line.append(['#', 'S', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
		self.__line.append(['#', '.', '#', '#', '#', '.', '#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#'])
		self.__line.append(['#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '#', '.', '.', '.', '#', '.', '#'])
		self.__line.append(['#', '.', '#', '.', '#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#'])
		self.__line.append(['#', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '#', '.', '#'])
		self.__line.append(['#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '#', '.', '.', '.', '#', '.', '#'])
		self.__line.append(['#', '.', '#', '.', '#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#'])
		self.__line.append(['#', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '#', '.', '#'])
		self.__line.append(['#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '#', '.', '.', '.', '#', '.', '#'])
		self.__line.append(['#', '.', '#', '.', '#', '.', '#', '#', '#', '#', '#', '.', '#', '#', '#', '.', '#'])
		self.__line.append(['#', '.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '#', '.', '#'])
		self.__line.append(['#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '#', '#', '#', '.', '#', '.', '#'])
		self.__line.append(['#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '#', 'E', '.', '.', '.', '.', '#'])
		self.__line.append(['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'])

		'''self.__line.append(['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'])
		self.__line.append(['#', 'S', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
		self.__line.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
		self.__line.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
		self.__line.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
		self.__line.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
		self.__line.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
		self.__line.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'E', '#'])
		self.__line.append(['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'])'''

		'''self.__line.append(['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'])
		self.__line.append(['#', 'S', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', 'E', '#'])
		self.__line.append(['#', '.', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
		self.__line.append(['#', '.', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
		self.__line.append(['#', '.', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
		self.__line.append(['#', '.', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
		self.__line.append(['#', '.', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
		self.__line.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
		self.__line.append(['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'])'''

		'''self.__line.append(['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'])
		self.__line.append(['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
		self.__line.append(['#', '.', '#', '#', '#', '.', '#', '#', '#', '#', '#', '.', '#', '.', '.', '.', '#'])
		self.__line.append(['#', '#', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '#', '#', '.', '#'])
		self.__line.append(['#', '.', '.', '#', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', 'S', '#'])
		self.__line.append(['#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '#', '#', '#', '.', '#'])
		self.__line.append(['#', '.', '#', '.', '#', '.', '#', '.', '#', '#', '#', '#', '#', '.', '.', '.', '#'])
		self.__line.append(['#', 'E', '#', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'])
		self.__line.append(['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'])'''

	def printmaze(self):
		for i in range(len(self.__line)):
			for j in range(len(self.__line[0])):
				print(self.__line[i][j], end="")
			print()
		print("\n\n")

	def setvisited(self, coord):
		self.__visitedlist.append(coord)

	def checkvisited(self, coord):
		if coord in self.__visitedlist:
			return 1
		return 0

	def genstartend(self):                    # Finds all "." on the maze and makes a Node object with their coordinate
		for i in range(1, len(self.__line) - 1):  # Finds start and end of the maze
			for j in range(1, len(self.__line[0]) - 1):
				if self.__line[i][j] == "S":
					self.__startcoord = (j, i)
				elif self.__line[i][j] == "E":
					self.__endcoord = (j, i)
	
	def getStart(self):
		return self.__startcoord
	
	def getEnd(self):
		return self.__endcoord

	def checkaround(self, node, hType):  # Takes a node, returns a list of all neighboring nodes that have not been visited
		hlist = []
		if self.checkvisited((node.getx(), node.gety() - 1)) == 0 and \
				(self.__line[node.gety() - 1][node.getx()] == "." or self.__line[node.gety() - 1][node.getx()] == "E"):
			hlist.append(Node((node.getx(), node.gety() - 1), self.__endcoord, hType, node))
		if self.checkvisited((node.getx() + 1, node.gety())) == 0 and \
				(self.__line[node.gety()][node.getx() + 1] == "." or self.__line[node.gety()][node.getx() + 1] == "E"):
			hlist.append(Node((node.getx() + 1, node.gety()), self.__endcoord, hType, node))
		if self.checkvisited((node.getx(), node.gety() + 1)) == 0 and \
				(self.__line[node.gety() + 1][node.getx()] == "." or self.__line[node.gety() + 1][node.getx()] == "E"):
			hlist.append(Node((node.getx(), node.gety() + 1), self.__endcoord, hType, node))
		if self.checkvisited((node.getx() - 1, node.gety())) == 0 and \
				(self.__line[node.gety()][node.getx() - 1] == "." or self.__line[node.gety()][node.getx() - 1] == "E"):
			hlist.append(Node((node.getx() - 1, node.gety()), self.__endcoord, hType, node))

		for i in hlist:
			if i.getcoord() == self.__endcoord:
				return i.getcoord(), i
			self.__line[i.gety()][i.getx()] = '*'
		return hlist
	
	def drawPath(self, path):
		for i in path:
			self.__line[i[1]][i[0]] = '*'


class Simulation:
	
	def __init__(self):
		self.agent = Agent()
		self.env = Environment()
	
	def simulate(self, hstr):
		self.env.resetmaze()
		self.env.printmaze()
		self.env.genstartend()
		
		self.agent.sense(self.env)
		length = self.agent.think(hstr)
		self.agent.act(self.env)
		print("Heuristic: ", hstr)
		print("Path length: ", length)

if __name__ == "__main__":
	start_Time = time.time()
	sim = Simulation()
	sim.simulate('euclidean')
	print("Total time was: " + str(time.time() - start_Time) + " sec.")

