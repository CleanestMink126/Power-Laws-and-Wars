import numpy as np
import matplotlib.pyplot as plt
import math

np.seterr(divide='ignore', invalid='ignore')
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

    def __init__(self, actorNum, pos):
        self.borderStates = {} #k = stateID v = set of position representing borders
        self.borderStateRes = {} #k = stateID v = total res that each enemey has put against this actor
        self.borderStateSelf = {} #k = stateID v = total res that this actor has put against each enemy k
        self.borderStateAttackProb = {} #k = stateID, v = attackProbability of this actor against state k

        self.warStates = {} #k = state we are at war with v = total damage
        self.totalEnemy = 0 # total enemy resources
        self.totalWar = 0 # totla resources of peop (adjusted by lowest value)
        self.numTotalBorders = 0
        self.actorNum = actorNum
        self.capital = pos
        self.provinces = {pos: Province(pos)} #k = pos v = province obj
        self.borders = {pos}#list of border states
        self.probexpand =  np.random.ranf()/3 + .1 # probability to expand
        self.fixesRes = .5
        self.extraRes = 0


    def addProvince(self, pos, province, warObj, res = 0):
        warObj.image[pos[0],pos[1],:] = warObj.dictCols[self.actorNum] #reset value in color map
        borders, _ = warObj.numBorder(self.actorNum, pos) #get borders
        province.numBorders = len(borders)
        province.updateDist(self.capital)
        province.res = res
        if len(borders): # add t dictionaries
            self.borders.add(pos)
        self.provinces[pos] = province


    def removeProvince(self, pos,warObj):  #pretty straightforward. removes from dictionaries and returns province
        if pos in self.borders:
            self.borders.remove(pos)
            _ , same = warObj.numBorder(self.actorNum, pos)
            for i in same:
                if i not in self.borders:
                    self.borders.add(i)
        return self.provinces.pop(pos)

    def updateBorder(self, k,warObj):
        totalborder = 0
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
                        if (not self.minV or diffBorder < self.minV):#check if min
                            self.minV = diffBorder
                else:
                    self.borderStates[state] = {k}
                    self.borderStateRes[state] = warObj.actorDict[state].provinces[b].res
                    if state in self.warStates:
                        totalborder += 1
                        diffBorder = (warObj.actorDict[state].provinces[b].res - self.provinces[k].res)
                        if (not self.minV or diffBorder < self.minV):
                            self.minV = diffBorder
        return totalborder

    def updateSelfBorders(self,warObj):
        for k,v in self.borderStateRes.items():#check border value from other person in each case
            if self.actorNum in warObj.actorDict[k].borderStateRes:
                self.borderStateSelf[k] = warObj.actorDict[k].borderStateRes[self.actorNum]
            else:
                print("COULD NOT FIND SELF IN COUNTERPART")
                self.borderStateSelf[k] = self.borderStateRes[k]#this is trash and should not happen often
        self.totalCurrentRes=sum(v for v in self.borderStateSelf.values())

    def updateBorders(self,warObj):
        self.borderStateRes = {}
        self.borderStates = {}
        self.borderStateSelf = {}
        self.totalEnemy = 0
        self.totalWar = 0
        borderList = list(self.borders)#get a list of the border states
        totalborder = 0#total borders with a warring state found
        self.minV = None#greatest advantage over a warring state
        for k in borderList:
            totalborder += self.updateBorder(k,warObj)
                    # print(self.borderStateRes)
        self.totalEnemy = sum(self.borderStateRes.values())
        if self.minV: self.totalWar = sum([self.borderStateRes[x] for x,v in self.warStates.items() if x in self.borderStateRes]) + totalborder * -1 * self.minV
        if not self.totalEnemy: self.totalEnemy = 0


    def distributeResources(self, totalRes,warObj):
        # print('TOTAL RES:',totalRes)
        # print('TOTAL WAR:',self.totalWar)
        borderList = list(self.borders)
         #these variables
        #mean nothing by themself I just multiplied out the constants at the beginning
        #of the loop rather than inside the loop
        fixedRate = 0
        variableRate = 0
        # print('TOTAL ENEMY:',self.totalEnemy)
        if self.totalWar and self.totalEnemy:
            variableRate =((1-self.fixesRes)*totalRes)/self.totalWar
            fixedRate = (self.fixesRes*totalRes)/self.totalEnemy
        elif self.totalEnemy:
            fixedRate = (totalRes)/self.totalEnemy
        for k in borderList:
            borders, same = warObj.numBorder(self.actorNum, k) #find borders
            oldRes = self.provinces[k].res
            if not len(borders):#if there are no borders get rid of it
                self.borders.pop(k)
            else:
                for b in borders:
                    state = warObj.npBoard[b]#get the state each border belongs to
                    eRes = warObj.actorDict[state].provinces[b].res#get that provinces resources
                    self.provinces[k].res += fixedRate * eRes #scale according to current resources
                    if state in self.warStates:
                        self.provinces[k].res += (variableRate) * (eRes - self.provinces[k].res - self.minV)# add more if they are at war

    def reallocateExtra(self,warObj):
        totalColleted = 0
        for province in self.provinces.values():
            if province.res != 0 and (province.pos not in self.borders):
                totalColleted += province.res * warObj.distanceFunc(province.distToCapital)
                province.res = 0
        self.extraRes = totalColleted

    def getFlanks(self, pos, enemyNum, warObj):
        borders, same = warObj.numBorder(enemyNum, pos)
        listFlanks = []
        for border in borders:
            if border in self.provinces:
                listFlanks.append(self.provinces[border])
        return listFlanks

    def actorBattle(self,k,enemyActor,warObj):
        borders,_ = warObj.numBorder(self.actorNum, k) #find eneemys that are adjacent

        for border in borders: #for all the enemies near the border province
            if border in enemyActor.provinces: #
                flanks = self.getFlanks(border,enemyActor.actorNum, warObj)
                enemyProvince = enemyActor.provinces[border]

                if k in self.provinces:
                    conquered = warObj.battle(flanks,enemyProvince)#fight!
                else:
                    conquered=0
                if conquered:#if there is a loser
                    # print("CONQUERED")
                    warObj.switchProvince(border, enemyActor,self,k)

    def wageWar(self, warObj):
        enemies =list(self.warStates.keys())
        for enemy in enemies:#for every enemy
            if enemy in self.borderStates:
                enemyActor = warObj.actorDict[enemy]
                # print(enemy)
                borderStates = list(self.borderStates[enemy])
                for k in borderStates:#find all border states next to this  enemy
                    self.actorBattle(k,enemyActor,warObj)
            else:
                self.borderStates.pop(enemy,None)

    def updateProbAttack(self):
        """Defines probability of Attacking an enemey state based on
        how much I allocated against the enemy / how much the enemy has allocated against you """
        borderStateRes = self.borderStateRes #k = stateID v = total res
        borderStateSelf = self.borderStateSelf
        enemyStates = list(borderStateRes.keys())
        for actor in enemyStates:
            if len(self.borderStates[actor]) == 0:
                self.borderStateRes.pop(actor,None)
                self.borderStateSelf.pop(actor,None)
                self.borderStateAttackProb.pop(actor,None)
            else:
                # rate = borderStateSelf[actor] / borderStateRes[actor]

                # print('Attack prob-------------')
                # print('TOP:', borderStateSelf[actor] )
                # print('BOTTOM:', borderStateRes[actor])
                self.borderStateAttackProb[actor] = self.sigmoid(borderStateSelf[actor],borderStateRes[actor])

    def declareWar(self,warObj):
        for k,v in self.borderStateAttackProb.items():
            if k in self.warStates:
                self.findPeace(k, warObj)
            elif k not in self.warStates and np.random.ranf() < v:
                self.warStates[k] = 0
                warObj.actorDict[k].warStates[self.actorNum] = 0

    def findPeace(self,enemyNum,warObj):
        warDamages = self.warStates[enemyNum]
        enemy = warObj.actorDict[enemyNum]
        if self.sigmoidPeace(self.totalCurrentRes,warDamages) and self.sigmoidPeace(enemy.totalCurrentRes,warDamages):
            v = self.warStates[enemyNum]
            v2= enemy.warStates[self.actorNum]
            self.warStates.pop(int(enemyNum))
            enemy.warStates.pop(self.actorNum)
            print('DIFFERENCE:', abs(v - v2))
            warObj.warDamages.append(v)

    def sigmoidPeace(self, p1, p2):
        if p1 == 0: return 0
        if p2 == 0: return 1
        rate = p1 / p2
        val =  1 / (1 + np.exp((10-rate)*3))
        # print(val)
        if math.isnan(val):
            val = 0
        randnum = np.random.ranf()
        return val > randnum

    def sigmoid(self, p1,p2):
        # print('R',rate)
        if p1 == 0: return 0
        if p2 == 0: return 1
        rate = p1 / p2
        val =  1 / (1 + np.exp((3-rate)*3))
        # print(val)
        if math.isnan(val):
            val = 0
        return val

class War2D:
    """Implements War"""
    initStage= True
    numberProvinces = 0
    def __init__(self, boardSize, numberPlayers):
        """Initializes the attributes.

        """
        self.totalSteps = 0
        self.warDamages = []
        self.boardSize = boardSize
        self.totalSquares = boardSize**2
        self.numberPlayers = numberPlayers
        self.npBoard = np.zeros((boardSize,boardSize), np.uint32)#board of actor ID and positions of provinces
        self.actorDict = {} # k: actorID, v: actorObjects
        self.dictCols = {0:(0.,0.,0.)} #dictionary relating actor ID and color
        self.FIXED_RES = 1 # constant for initial resource allocatead to each provinces
        self.maxDistance = math.sqrt(2)*self.boardSize
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
        # print(self.image)

    def show(self):#show the current state of the board
        plt.imshow(self.image)
        plt.show()

    def show2(self):#show the current state of the board
        plt.imshow(self.image2)
        plt.show()

    def switchProvince(self,pos, loser, winner,k):#UPDATE
        province = loser.removeProvince(pos, self)
        self.npBoard[pos] = winner.actorNum#
        borders,same = self.numBorder(winner.actorNum, k)
        if len(borders):

            newRes = winner.provinces[k].res / 2
            winner.provinces[k].res = newRes
        else:
            newRes = winner.provinces[k].res
            winner.provinces[k].res = 0
        # print(newRes)
        winner.addProvince(pos, province,self,newRes)
        if pos == loser.capital:
            self.conquer(loser)
        if pos in loser.borderStates[winner.actorNum]:
            loser.borderStates[winner.actorNum].remove(pos)
            for border in borders:
                if border in loser.provinces:
                    loser.borderStates[winner.actorNum].add(border)
            for border in same:
                borders2,_ = self.numBorder(winner.actorNum, border)
                if not len(borders2) and border in winner.borderStates[loser.actorNum]:
                    winner.borderStates[loser.actorNum].remove(border)


    def conquer(self,loser):
        for i in loser.borders:
            loser.provinces[i].res = 0
        for k in loser.warStates.keys():
            self.warDamages.append(loser.warStates[k])
        #//TODO

    def colorCodeProvinces(self):
        maxv = 0
        for x in range(self.boardSize):
            for y in range(self.boardSize):
                actor = self.actorDict[self.npBoard[x,y]]
                province = actor.provinces[(x,y)]
                if math.isnan(province.res) or province.res < 0:
                    self.image2[x,y,:] = [0.,0.,0.]
                else:
                    self.image2[x,y,:] = [math.log(province.res+1),math.log(province.res+1), math.log(province.res+1)]
                if province.res > maxv: maxv = math.log(province.res+1)

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

    def updateActorBorders(self):
        for actor in self.actorDict.values():#loop through and expand actors. should be shuffled in future
            actor.updateBorders(self)

    def updateActorSelfBorders(self):
        for actor in self.actorDict.values():#loop through and expand actors. should be shuffled in future

            actor.updateSelfBorders(self)
            actor.updateProbAttack()

    def updateActorDist(self):

        for actor in self.actorDict.values():#loop through and expand actors. should be shuffled in future
            if self.npBoard[actor.capital] == actor.actorNum:
                totalRes = np.sum([self.FIXED_RES * self.distanceFunc(province.distToCapital) for province in actor.provinces.values()]) + actor.extraRes
                actor.distributeResources(totalRes,self)
                actor.extraRes = 0
            else:
                totalRes = 0
                actor.distributeResources(totalRes,self)

    def garbageCollection(self):
        for actor in self.actorDict.values():#
            if self.npBoard[actor.capital] == actor.actorNum:
                actor.reallocateExtra(self)

    def distanceFunc(self, distToCapital):
        return (self.maxDistance - distToCapital) / self.maxDistance

    def actorWars(self):
        for actor in self.actorDict.values():#loop through and expand actors. should be shuffled in future
            actor.declareWar(self)
            actor.wageWar(self)

    def step(self):
        """Executes one time step."""

        if self.initStage:
            for i in self.actorDict.values():#loop through and expand actors. should be shuffled in future
                self.actorExpand(i)
            if self.numberProvinces >= self.totalSquares:
                self.initRes()
                self.initStage = False
        else:
            self.totalSteps += 1
            self.updateActorBorders()
            self.updateActorSelfBorders()
            self.updateActorDist()
            self.actorWars()
            if not self.totalSteps % 5:
                self.garbageCollection()
            self.colorCodeProvinces()

    def battle(self, flank, p2):
        """Defines the battle behavior for province p1 and province p2"""
        BATTLE_DAMAGE = 0.1 # battle damage
        a1 = self.npBoard[flank[0].pos] # the actor ID of province p1
        a2 = self.npBoard[p2.pos] # the actor ID of province p2
        # probAttacking = self.actorDict[a1].borderStateAttackProb[a2] # probability that p1 will attack p2, macroscopic level
        # print('Win Prob')
        # print('TOP:', p1.res )
        # print('BOTTOM:', p2.res)
        flankRes = sum(x.res for x in flank)
        probWinning = self.actorDict[a1].sigmoid(flankRes , p2.res) # probability that p1 will win against p2, microscopic province level

        randProb = np.random.ranf()
        while probWinning > randProb: # won
            for x in flank:
                x.res -= x.res * BATTLE_DAMAGE
            p2.res -= flankRes * BATTLE_DAMAGE
            # print('p1.res:', p1.res)
            self.actorDict[a1].warStates[a2] += flankRes * BATTLE_DAMAGE
            self.actorDict[a2].warStates[a1] += flankRes * BATTLE_DAMAGE
            randProb = np.random.ranf()

            if probWinning < randProb:
                return False
            elif p2.res <= 0:
                p2.res = 0
                return True
            # print('Win Prob')
            # print('TOP:', p1.res )
            # print('BOTTOM:', p2.res)
            flankRes = sum(x.res for x in flank)
            probWinning = self.actorDict[a1].sigmoid(flankRes , p2.res) # probability that p1 will win against p2, microscopic province level
            randProb = np.random.ranf()
        return False

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
            totalRes = np.sum([self.FIXED_RES * self.distanceFunc(province.distToCapital) for province in actor.provinces.values()])
            borderProvinces = list(actor.borders)
            for borderProvince in borderProvinces:
                actor.provinces[borderProvince].res = int(totalRes * actor.provinces[borderProvince].numBorders / actor.numTotalBorders)

if __name__ == "__main__":

    mywar = War2D(100, 10)
    for i in range(100):
        mywar.step()
        if not i % 10:
            mywar.show()
    mywar.show()
    mywar.show2()
