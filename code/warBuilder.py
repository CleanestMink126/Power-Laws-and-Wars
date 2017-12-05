import numpy as np
import matplotlib.pyplot as plt
class Province:
    '''Province class that contains the number of borders and contained resources'''

    def __init__(self, pos):
        self.res = 0
        self.numBorders = 0
        self.distToCapital = 0
        self.pos = pos

    def updateDist(self, capitalPos):
        self.distToCapital = np.sqrt((self.pos[0]-capitalPos[0])**2 + (self.pos[1]-capitalPos[1])**2)

class Actor:
    '''Actor class that contains the ID, capital position and dictionaries of its
    provinces and borders'''
    borderStates = {} #k = stateID v = set of position representing borders
    borderStateRes = {} #k = stateID v = total res that each enemey has put against this actor
    borderStateSelf = {} #k = stateID v = total res that this actor has put against each enemy k
    borderStateAttackProb = {} #k = stateID, v = attackProbability of this actor against state k

    warStates = {} #k = state we are at war with v = total damage
    totalEnemy = 0 # total enemy resources
    totalWar = 0 # totla resources of peop (adjusted by lowest value)
    numTotalBorders = 0
    def __init__(self, actorNum, pos):
        self.actorNum = actorNum
        self.capital = pos
        self.provinces = {pos: Province(pos)} #k = pos v = province obj
        self.borders = {pos}#list of border states
        self.probexpand =  np.random.ranf()/4 + .25 # probability to expand
        self.fixesRes = .5


    def addProvince(self, pos, province, warObj):
        warObj.image[pos[0],pos[1],:] = warObj.dictCols[self.actorNum] #reset value in color map
        borders, _ = warObj.numBorder(self.actorNum, pos) #get borders
        province.numBorders = len(borders)
        province.updateDist(self.capital)
        province.res = 0
        if len(borders): # add t dictionaries
            self.borders.add(pos)
        self.provinces[pos] = province


    def removeProvince(self, pos,warObj):  #pretty straightforward. removes from dictionaries and returns province
        if pos in self.borders:
            self.borders.pop(pos)
            _ , same = warObj.numBorder(self.actorNum, pos)
            for i in same:
                if i not in self.borders:
                    borders.add(i)
        return provinces.pop(pos)

    def updateBorders(self,warObj):
        self.borderStateRes = {}
        self.borderStates = {}
        borderList = list(self.borders)#get a list of the border states
        totalborder = 0#total borders with a warring state found
        self.minV = None#greatest advantage over a warring state
        for k in borderList:
            borders,same = warObj.numBorder(self.actorNum, k)#find the borders for each border province
            self.provinces[k].numBorders = len(borders) #update the correstponding province
            if not len(borders):#if no borders remove the obj
                self.borders.remove(k)
            else:
                for b in borders:
                    state = warObj.npBoard[b]#get the state
                    if state in self.borderStates:#if state indexed
                        self.borderStates[state].add(k)#add border
                        self.borderStateRes[state] = self.borderStateRes.pop(state) + warObj.actorDict[state].provinces[b].res#add enemy resource
                        if state in self.warStates:#if warring with the state
                            totalborder += 1
                            diffBorder = (warObj.actorDict[state].provinces[b].res - self.provinces[k].res)#find diff
                            if (not minV or diffBorder < minV):#check if min
                                self.minV = diffBorder
                    else:
                        self.borderStates[state] = {k}
                        self.borderStateRes[state] = warObj.actorDict[state].provinces[b].res
                        if state in self.warStates:
                            totalborder += 1
                            diffBorder = (warObj.actorDict[state].provinces[b].res - self.provinces[k].res)
                            if (not minV or diffBorder < minV):
                                self.minV = diffBorder
                    # print(self.borderStateRes)
        for k,v in self.borderStateRes.items():#check border value from other person in each case
            if self.actorNum in warObj.actorDict[k].borderStateRes:
                res = warObj.actorDict[k].borderStateRes[self.actorNum]
                self.borderStateSelf[k] = res
            else:
                self.borderStateSelf[k] = self.borderStateRes[k]
        self.totalEnemy = sum(self.borderStateRes.values())
        if self.minV: self.totalWar = sum([self.borderStateRes[x] for x,v in self.warStates]) + totalborder * -1 * self.minV

    def distributeResources(self, totalRes,warObj):
        borderList = list(self.borders)
        fixedRate = (self.fixesRes*totalRes)/self.totalEnemy #these variables
        #mean nothing by themself I just multiplied out the constants at the beginning
        #of the loop rather than inside the loop
        if self.totalWar: variableRate =((1-self.fixesRes)*totalRes)/self.totalWar
        for k in borderList:
            borders,same = warObj.numBorder(self.actorNum, k)
            if not len(borders):
                self.borders.pop(k)
            else:
                for b in borders:
                    state = warObj.npBoard[b]
                    eRes = warObj.actorDict[state].provinces[b].res
                    self.provinces[k].res += fixedRate * eRes
                    if state in self.warStates:
                        self.provinces[k].res += (variableRate -self.minV) * eRes

    def updateProbAttack(self):
        """Defines probability of Attacking an enemey state based on
        how much I allocated against the enemy / how much the enemy has allocated against you """
        borderStateRes = self.borderStateRes #k = stateID v = total res
        borderStateSelf = self.borderStateSelf
        enemyStates = list(borderStateRes.keys())
        print("SELF",borderStateSelf)
        print("OTHER",borderStateRes)
        print("PARTS", self.borderStates)
        for actor in enemyStates:
            rate = borderStateSelf[actor] / borderStateRes[actor]
            self.borderStateAttackProb[actor] = self.sigmoid(rate)

    def sigmoid(self, rate):
        return 1 / (1 + np.exp(3-rate))

class War2D:
    """Implements Conway's Game of Life."""
    initStage= True
    numberProvinces = 0
    def __init__(self, boardSize, numberPlayers):
        """Initializes the attributes.

        """
        self.boardSize = boardSize
        self.totalSquares = boardSize**2
        self.numberPlayers = numberPlayers
        self.npBoard = np.zeros((boardSize,boardSize), np.uint32)#board of actor ID and positions of provinces
        self.actorDict = {}
        self.dictCols = {0:(0.,0.,0.)} #dictionary relating actor ID and color
        self.FIXED_RES = 100 # constant for initial resource allocatead to each provinces
        positions = np.random.choice(boardSize*boardSize, numberPlayers)#randomly initialize actors
        for i,v in enumerate(positions):#make the actors and add them to variables
            pos = (v%boardSize,v//boardSize)
            self.actorDict[i+1] = Actor(i+1,pos)
            self.npBoard[pos] = i+1
            self.dictCols[i+1] = [np.random.ranf(),np.random.ranf(),np.random.ranf()]
            self.numberProvinces += 1

        self.image = np.zeros((boardSize, boardSize,3), np.float32)#create graphical display board
        self.image2 = np.zeros((boardSize, boardSize,3), np.float32)
        # for i,v in enumerate(self.npBoard):
        #     for j,w in enumerate(v):
        #         self.image[i,j,:] = self.dictCols[w]
        print(self.image)

    def show(self):#show the current state of the board
        plt.imshow(self.image)
        plt.show()

    def show2(self):#show the current state of the board
        plt.imshow(self.image2)
        plt.show()

    def colorCodeProvinces(self):
        maxv = 0
        for x in range(self.boardSize):
            for y in range(self.boardSize):
                actor = self.actorDict[self.npBoard[x,y]]
                province = actor.provinces[(x,y)]
                self.image2[x,y,:] = [province.res, province.res, province.res]
                if province.res > maxv: maxv = province.res

        self.image2 /= maxv

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
        borders = []
        same = []
        for i in neighbors:
            if self.npBoard[i] != num:
                borders.append(i)
            else:
                same.append(i)
        return borders, same

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
            if self.numberProvinces >= self.totalSquares:
                self.initRes()
                self.initStage = False
        else:
            self.colorCodeProvinces()
            for actor in self.actorDict.values():#loop through and expand actors. should be shuffled in future
                actor.updateBorders(self)
                totalRes = self.FIXED_RES * len(actor.provinces)
                actor.distributeResources(totalRes, self)
                actor.updateProbAttack()
                # print(actor.totalEnemy)
                # print(actor.borderStateAttackProb)


    def actorExpand(self,actor):
        borderList = list(actor.borders)
        # print(borderList)
        for i in borderList:
            pBool, pos = self.provinceExpand(i, actor.actorNum, actor.probexpand)
            while pBool:# keep expanding until the probablity returns false
                self.npBoard[pos] = actor.actorNum
                newProvince = Province(pos)
                actor.addProvince(pos, newProvince, self)
                self.numberProvinces += 1
                pBool, pos = self.provinceExpand(pos, actor.actorNum,actor.probexpand)

    def provinceExpand(self,pos, num,prob):
        # print(pos)
        if prob < np.random.ranf():
            borderList = self.numZero(pos)
            if len(borderList):
                choice = np.random.choice(len(borderList),1)
                return True, borderList[choice[0]]
        return False, None

    def initRes(self):
        actorList = list(self.actorDict.values())
        for actor in actorList:
            actor.numTotalBorders = 0
            borderList = list(actor.borders)
            for k in borderList:
                borders,same = self.numBorder(actor.actorNum, k)
                actor.provinces[k].numBorders = len(borders)
                actor.numTotalBorders += len(borders)
            totalRes = self.FIXED_RES * len(actor.provinces)
            borderProvinces = list(actor.borders)
            for borderProvince in borderProvinces:
                actor.provinces[borderProvince].res = int(totalRes * actor.provinces[borderProvince].numBorders / actor.numTotalBorders)

if __name__ == "__main__":

    mywar = War2D(100, 10)
    for i in range(60):
        mywar.step()
        # if not i % 10:
        #     mywar.show()
    mywar.show()
    mywar.show2()
