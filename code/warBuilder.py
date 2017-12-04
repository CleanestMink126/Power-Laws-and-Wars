import numpy as np
import matplotlib.pyplot as plt
class Province:

    '''Province class that contains the number of borders and contained resources'''

    def __init__(self):
        self.res = 0
        self.numBorders = 0

    def updateRes(capital, res):
        pass

class Actor:

    '''Actor class that contains the ID, capital position and dictionaries of its
    provinces and borders'''
    def __init__(self,actorNum,pos):
        self.actorNum = actorNum
        self.capital = pos
        self.provinces = {}
        self.borders = {pos: Province()}
        self.probexpand = 0.5 # probability to expand

    def addProvince(self, pos, province, warObj):
        numborders = warObj.numBorder(self.actorNum, pos) #get number of borders
        warObj.image[pos[0],pos[1],:] = warObj.dictCols[self.actorNum] #reset value in color map
        province.borders = numborders
        if numborders:#add t dictionaries
            self.borders[pos] = province
        self.provinces[pos] = province

    def removeProvince(self, pos):#pretty straightforward. removes from dictionaries and returns province
        if pos in self.borders:
            borders.pop(pos)
        return provinces.pop(pos)



class War2D:
    """Implements Conway's Game of Life."""
    initStage= True
    def __init__(self, boardSize, numberPlayers):
        """Initializes the attributes.

        """
        self.boardSize = boardSize
        self.numberPlayers = numberPlayers
        self.npBoard = np.zeros((boardSize,boardSize), np.uint32)#board of actor ID and positions of provinces
        self.actorDict = {}
        self.dictCols = {0:(0.,0.,0.)}#dictionary relating actor ID and color
        positions = np.random.choice(boardSize*boardSize, numberPlayers)#randomly initialize actors
        for i,v in enumerate(positions):#make the actors and add them to variables
            pos = (v%boardSize,v//boardSize)
            self.actorDict[i+1] = Actor(i+1,pos)
            self.npBoard[pos] = i+1
            self.dictCols[i+1] = [np.random.ranf(),np.random.ranf(),np.random.ranf()]

        self.image = np.zeros((boardSize, boardSize,3), np.float32)#create graphical display board
        for i,v in enumerate(self.npBoard):
            for j,w in enumerate(v):
                self.image[i,j,:] = self.dictCols[w]
        print(self.image)

    def show(self):#show the current state of the board
        plt.imshow(self.image)
        plt.show()
    def getneighbors(self,pos):#get the neighbors of a position
        boolarr = [pos[0]>0,pos[0]<self.boardSize-1,pos[1]>0,pos[1]<self.boardSize-1]
        posarr = [(pos[0]-1,pos[1]),(pos[0]+1,pos[1]),(pos[0],pos[1]-1),(pos[0],pos[1]+1)]
        return [posarr[i] for i,v in enumerate(boolarr) if v]

    def numBorder(self,num, pos):#get the neighbors that are different from the given number
        if self.npBoard[pos] != num:
            print(self.npBoard[pos])
            print(num)
            print('ACTOR NUM DOES NOT MATCH POS')
        neighbors = self.getneighbors(pos)
        borders = 0
        for i in neighbors:
            if self.npBoard[i] != num:
                borders += 1
        return borders

    def numZero(self,pos): #get unoccupied neighbors
        neighbors = self.getneighbors(pos)
        borders = []
        for i in neighbors:
            if self.npBoard[i] == 0:
                borders.append(i)
        return borders


    def step(self):
        """Executes one time step."""
        if self.initStage:
            for i in self.actorDict.values():#loop through and expand actors. should be shuffled in future
                self.actorExpand(i)
        # if self.prepStage:
            pass
        # if self.battleStage:
            pass

    def actorExpand(self,actor):
        borderList = list(actor.borders.keys())
        for i in borderList:
            pBool, pos = self.provinceExpand(i, actor.actorNum,actor.probexpand)
            while pBool:#keep expanding until the probablity returns false
                self.npBoard[pos] = actor.actorNum
                actor.addProvince(pos, Province(),self)
                pBool, pos = self.provinceExpand(pos, actor.actorNum,actor.probexpand)

    def provinceExpand(self,pos, num,prob):
        if prob < np.random.ranf():
            borderList = self.numZero(pos)
            if len(borderList):
                choice = np.random.choice(len(borderList),1)
                return True, borderList[choice[0]]
        return False, None

    def interactBattle():
        pass
    def battle():
        pass
if __name__ == "__main__":

    mywar = War2D(20, 20)
    for i in range(10):
        mywar.step()
        mywar.show()
