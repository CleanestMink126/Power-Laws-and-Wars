import numpy as np
import matplotlib.pyplot as plt
class Province:
    res = 0
    borders = 0
    def __init__(self):
        pass

class Actor:
    def __init__(self,actorNum,pos):
        self.actorNum = actorNum
        self.capital = pos
        self.provinces = {}
        self.borders = {pos: Province()}
        self.probexpand = 0.5

    def add_province(self,pos, province,warObj):
        numborders = warObj.numBorder(self.actorNum,pos)
        province.borders = numborders
        if numborders:
            self.borders[pos] = province
        self.provinces[pos] = province

    def remove_province(self,pos):
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
        self.npBoard = np.zeros((boardSize,boardSize), np.uint32)
        self.actorDict = {}
        self.dictCols = {0:(0.,0.,0.)}
        positions = np.random.choice(boardSize*boardSize, numberPlayers)
        for i,v in enumerate(positions):
            pos = (v%boardSize,v//boardSize)
            self.actorDict[i+1] = Actor(pos)
            self.npBoard[pos] = i+1
            self.dictCols[i+1] = [np.random.ranf(),np.random.ranf(),np.random.ranf()]

        self.image = np.zeros((boardSize, boardSize,3), np.float32)
        for i,v in enumerate(self.npBoard):
            for j,w in enumerate(v):
                self.image[i,j,:] = self.dictCols[w]
        print(self.image)
        plt.imshow(self.image)
        plt.show()
        return self.image

    def getneighbors(self,pos):
        boolarr = [pos[0]>0,pos[0]<self.boardSize-1,pos[1]>0,pos[1]<self.boardSize-1]
        posarr = [(pos[0]-1,pos[1]),(pos[0]+1,pos[1]),(pos[0],pos[1]-1),(pos[0],pos[1]+1)]
        return [posarr[i] for i,v in enumerate(boolarr) if v]

    def numBorder(self,num, pos):
        if self.npBoard[pos] != num:
            print('ACTOR NUM DOES NOT MATCH POS')
        neighbors = self.getneighbors(pos)
        borders = 0
        for i in neighbors:
            if self.npBoard[i] != num:
                borders += 1
        return borders

    def numZero(self,pos):
        if self.npBoard[pos] != num:
            print('ACTOR NUM DOES NOT MATCH POS')
        neighbors = self.getneighbors(pos)
        borders = []
        for i in neighbors:
            if self.npBoard[i] == 0:
                borders.append(i)
        return borders


    def step(self):
        """Executes one time step."""
        if initStage:
            for i in self.actorDict.keys():

    def actorExpand(self,actor):
        for i in actor.borders.keys():
            while provinceExpand(i, prob):
                continue
    def provinceExpand(self,pos, prob):
        if prob < np.random.ranf():
            self.numZero(pos)
            return True
        return False


War2D(20, 20)
