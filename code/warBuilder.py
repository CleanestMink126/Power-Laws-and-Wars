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

    def addProvince(self,pos, province,warObj):
        numborders = warObj.numBorder(self.actorNum,pos)
        warObj.image[pos[0],pos[1],:] = warObj.dictCols[self.actorNum]
        province.borders = numborders
        if numborders:
            self.borders[pos] = province
        self.provinces[pos] = province

    def removeProvince(self,pos):
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
            self.actorDict[i+1] = Actor(i+1,pos)
            self.npBoard[pos] = i+1
            self.dictCols[i+1] = [np.random.ranf(),np.random.ranf(),np.random.ranf()]

        self.image = np.zeros((boardSize, boardSize,3), np.float32)
        for i,v in enumerate(self.npBoard):
            for j,w in enumerate(v):
                self.image[i,j,:] = self.dictCols[w]
        print(self.image)

    def show(self):
        plt.imshow(self.image)
        plt.show()
    def getneighbors(self,pos):
        boolarr = [pos[0]>0,pos[0]<self.boardSize-1,pos[1]>0,pos[1]<self.boardSize-1]
        posarr = [(pos[0]-1,pos[1]),(pos[0]+1,pos[1]),(pos[0],pos[1]-1),(pos[0],pos[1]+1)]
        return [posarr[i] for i,v in enumerate(boolarr) if v]

    def numBorder(self,num, pos):
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

    def numZero(self,pos):
        neighbors = self.getneighbors(pos)
        borders = []
        for i in neighbors:
            if self.npBoard[i] == 0:
                borders.append(i)
        return borders


    def step(self):
        """Executes one time step."""
        if self.initStage:
            for i in self.actorDict.values():
                self.actorExpand(i)

    def actorExpand(self,actor):
        borderList = list(actor.borders.keys())
        for i in borderList:
            pBool, pos = self.provinceExpand(i, actor.actorNum,actor.probexpand)
            while pBool:
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

if __name__ == "__main__":
    
    mywar = War2D(20, 20)
    for i in range(10):
        mywar.step()
        mywar.show()
