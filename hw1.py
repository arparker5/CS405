'''
Dots and Boxes
By Andrew Parker
CS 405
2/11/19
Dr. Metzgar
'''

import random

class DefensiveAgent:                                         #Agent takes into account the opposing player's next move
    __score = 0

    def playturn(self):
        E1.playmove(self.pickmove())                        # Once a valid move is chosen, the move is played,
        point = E1.ifpoint("D")
        if point > 0:                            # then a point is added if a box is completed
            self.__score += point
            return 1
        return 0
    def pickmove(self):
        move1 = [0, 0]                                   #value 1 is point, value 2 is the move
        bestoppmove = [0, 0]
        bestmove = [-100, 0]

        if len(E1.getmovesleft()) > 2:
            for i in E1.getmovesleft():
                move2 = 0
                E1.settempcoordmap(i)
                move1[0] = E1.testpoint()
                move1[1] = i

                if move1[0] == 0:
                    for j in E1.getmovesleft():
                        E1.settempcoordmap(j)
                        oppmove = E1.testpoint()
                        if oppmove >= bestoppmove[0]:
                            bestoppmove[0] = oppmove
                            bestoppmove[1] = j
                        E1.undotempcoordmap(j)
                else:
                    for j in E1.getmovesleft():
                        E1.settempcoordmap(j)
                        move2 = E1.testpoint()
                        E1.undotempcoordmap(j)

                if move1[0] - bestoppmove[0] + move2 >= bestmove[0]:
                    bestmove = [move1[0], move1[1]]

                E1.undotempcoordmap(i)
        else:
            for i in E1.getmovesleft():
                E1.settempcoordmap(i)
                if E1.testpoint() > bestmove[0]:
                    bestmove[1] = i
                E1.undotempcoordmap(i)

        if bestmove[1] != 0:
            return bestmove[1]
        return int(random.choice(E1.getmovesleft()))

    def retscore(self):
        return self.__score


class OffensiveAgent:                               # Agent takes the move that gives the most amount of points, if no point, picks random
    __score = 0

    def playturn(self):
        E1.playmove(self.pickmove())                        # Once a valid move is chosen, the move is played,
        point = E1.ifpoint("O")
        if point > 0:                                      # then a point is added if a box is completed
            self.__score += point
            return 1
        return 0
    def pickmove(self):
        bestmove = [0, 0]                                   #value 1 is point, value 2 is the move
        for i in E1.getmovesleft():
            E1.settempcoordmap(i)
            if E1.testpoint() > bestmove[0]:
                bestmove[1] = i
            E1.undotempcoordmap(i)
        if bestmove[1] != 0:
            return bestmove[1]
        return int(random.choice(E1.getmovesleft()))

    def retscore(self):
        return self.__score

class RandAgent:                                            # Agent selects a random move every time

    __score = 0

    def playturn(self):
        E1.playmove(int(random.choice(E1.getmovesleft())))
        point = E1.ifpoint("R")
        if point > 0:
            self.__score += point
            return 1
        return 0

    def retscore(self):
        return self.__score

class Player:

    __score = 0

    def playturn(self):
        valid = 0
        x = 0
        print("Your turn! Input move")
        while valid == 0:
            x = input("-->")
            valid = E1.checkinput(int(x))                  # Checks if the input is valid
        E1.playmove(int(x))                                # Once a valid move is chosen, the move is played,
        point = E1.ifpoint("P")
        if point > 0:                                      # then a point is added if a box is completed
            self.__score += point
            return 1
        return 0

    def retscore(self):
        return self.__score

class Environment:

    __x = 0
    __linestate = []
    __boxeswon = []                             #stores lists of box states
    __boxcheck = []                     #stores perimeters of each box left
    __coordmap = {1121 : [0, 0]}      # key is line 'id', value 1 is index, value 2 is 'already used' bit, value 3 is the output
    __movesleft = {}

    def __init__ (self, x):
        self.__x = x

        for i in range(2*((x**2)-x)):       #Makes array of all the lines
            self.__linestate.append(" ")

        for i in range((x-1)**2):
            self.__boxeswon.append(" ")

        boxcount = 0
        for i in range(1, x):
            nextref = 1000+(i*100)+10+(i+1)
            boxcount += 1
            while boxcount % x != 0:
                self.__boxcheck.append([nextref, nextref + 9,nextref + 1010, nextref + 110, 0])
                nextref = self.__boxcheck[-1][2]
                boxcount += 1



        coordcount = 1121
        indexcount = 1
        firstinrow = 1121
        for i in range(0, self.__x - 2):                #Sets up coordinate system for first row
            coordcount += 1010
            self.__coordmap[coordcount] = [indexcount,0]
            indexcount += 1

        for i in range(0, self.__x - 1):                #Sets up coordinate system for the rest of the board
            coordcount = firstinrow - 9
            firstinrow = coordcount
            self.__coordmap[coordcount] = [indexcount,0]
            indexcount += 1
            for j in range(0, self.__x - 1):
                coordcount += 1010
                self.__coordmap[coordcount] = [indexcount,0]
                indexcount += 1

            coordcount = firstinrow + 110
            firstinrow = coordcount
            self.__coordmap[coordcount] = [indexcount,0]
            indexcount += 1
            for k in range(0, self.__x - 2):
                coordcount += 1010
                self.__coordmap[coordcount] = [indexcount,0]
                indexcount += 1

        self.__movesleft = self.__coordmap.copy()
    def printboard(self):                                           #Prints the current board state
        count = 0
        countb = 0


        print("Moves Left: ", end = "")
        for x in self.__movesleft:                               #Prints remaining moves left
            print(x, end = " ")
        print("\n")

        print(end="  ")
        for x in range(self.__x):                               #Prints top index row
            print(x+1, end = "   ")
        print()

        for x in range(0, self.__x):                                #Prints first row
            if x == 0:
                print(1, end = " ")
            print("x", end = " ")
            if x < (self.__x - 1) :
                print(self.__linestate[count], end = " ")
                count += 1

        for x in range(1, self.__x):                         #Prints all remaining rows
            print("\n", end = "  ")
            for z in range(0, self.__x):
                print(self.__linestate[count], end=" ")
                if z < self.__x - 1:
                    print(self.__boxeswon[countb], end = " ")
                    countb += 1
                count += 1
            print()
            print(x+1, end = " ")
            for y in range(0, self.__x):
                print("x", end=" ")
                if y < (self.__x - 1):
                    print(self.__linestate[count], end=" ")
                    count += 1
        print ("\n")

    def checkinput(self, x):                                       #Makes sure input is in dictionary and isn't already taken
        if x in self.__coordmap and self.__coordmap[x][1] != 1:
            return 1
        print("Invalid Input! Try again!")
        return 0

    def playmove(self, x):
        self.__coordmap[x][1] = 1
        if int(str(x)[1]) - int(str(x)[3]) == 0:
            self.__linestate[self.__coordmap[x][0]] = "-"
        else:
            self.__linestate[self.__coordmap[x][0]] = "|"

        del self.__movesleft[x]



    def ifpoint(self, playerid):                    #Checks to see if a point was made
        point = 0
        for i in range(len(self.__boxcheck)):
            if self.__boxcheck[i][4] == 0:
                if self.__coordmap[self.__boxcheck[i][0]][1] == 1 \
                        and self.__coordmap[self.__boxcheck[i][1]][1] == 1 \
                        and self.__coordmap[self.__boxcheck[i][2]][1] == 1 \
                        and self.__coordmap[self.__boxcheck[i][3]][1] == 1:
                    self.__boxcheck[i][4] = 1
                    self.__boxeswon[i] = playerid
                    point += 1
        return point

    def testpoint(self):                                #Tests the outcome of a move without doing it
        point = 0
        for i in range(len(self.__boxcheck)):
            if self.__boxcheck[i][4] == 0:
                if self.__coordmap[self.__boxcheck[i][0]][1] == 1 \
                        and self.__coordmap[self.__boxcheck[i][1]][1] == 1 \
                        and self.__coordmap[self.__boxcheck[i][2]][1] == 1 \
                        and self.__coordmap[self.__boxcheck[i][3]][1] == 1:
                    point += 1
        #print(point)
        return point

    def settempcoordmap(self, i):
        self.__coordmap[i][1] = 1
        del self.__movesleft[i]

    def undotempcoordmap(self, i):
        self.__coordmap[i][1] = 0
        self.__movesleft[i] = self.__coordmap[i].copy()

    def getmovesleft(self):
        return list(self.__movesleft.keys())

    def checkgameend(self):
        if len(self.__movesleft) == 0:
            return 1
        return 0



print("Dots and Boxes")
print("If you do not know the rules, look up 'dots and boxes' on wikipedia")
print("Selecting Players")
print("-----------------")
print("Select player 1! Type 'p' for human player, 'r' for an agent that plays randomly,")
print("'o' for an offensive agent, and 'd' for a defensive agent")
p1 = input("--> ")

humanp = 0
check = 1
while check == 1:
    check = 0
    if p1 == 'p':
        P1 = Player()
        player1name = 'Human Player 1'
        humanp = 1
    elif p1 == 'r':
        P1 = RandAgent()
        player1name = 'Random Agent 1'
    elif p1 == 'o':
        P1 = OffensiveAgent()
        player1name = 'Offensive Agent 1'
    elif p1 == 'd':
        P1 = DefensiveAgent()
        player1name = 'Defensive Agent 1'
    else:
        check = 1
        print("Invalid input! Try again!")
        p1 = input("--> ")

print("Now select player 2! Type 'p' for human player, 'r' for an agent that plays randomly,")
print("'o' for an offensive agent, and 'd' for a defensive agent")
p2 = input("--> ")
while p2 != 'p' and p2 != 'r' and p2 != 'o' and p2 != 'd':
    print("Invalid input! Try again!")
    p2 = input("--> ")

check = 1
while check == 1:
    check = 0
    if p2 == 'p':
        P2 = Player()
        player2name = 'Human Player 2'
        humanp = 1
    elif p2 == 'r':
        P2 = RandAgent()
        player2name = 'Random Agent 2'
    elif p2 == 'o':
        P2 = OffensiveAgent()
        player2name = 'Offensive Agent 2'
    elif p2 == 'd':
        P2 = DefensiveAgent()
        player2name = 'Defensive Agent 2'
    else:
        check = 1
        print("Invalid input! Try again!")
        p1 = input("--> ")


print("What size board do you want? Sizes available: 2 - 9. (type 3 for a 3x3 board, etc..)")
size = input("--> ")
while size.isalpha() or size.isspace() or int(size) < 2 or int(size) > 9:
    print("Invalid input! Try again!")
    size = input("--> ")

if humanp == 1:
    print("To draw a line from (1,1) - (1,2), type 1112")
    print("Always start drawing the line from top to bottom and from left to right")


E1 = Environment(int(size))
E1.printboard()


while  E1.checkgameend() != 1:
    while E1.checkgameend() == 0 and P1.playturn() == 1:
        E1.printboard()
    E1.printboard()

    while E1.checkgameend() == 0 and P2.playturn() == 1:
        E1.printboard()
    E1.printboard()


print("Game Over!")
print(player1name+ " Score: ", end = " ")
print(P1.retscore())
print(player2name + " Score: ", end = " ")
print(P2.retscore())
whowon = P1.retscore() - P2.retscore()
if whowon == 0:
    print("Tie!")
elif whowon > 0:
    print(player1name + " wins!")
else:
    print(player2name + " wins!")
