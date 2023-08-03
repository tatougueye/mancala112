###Mancala112 by Fatou Gueye###
from cmu_graphics import *
import random

class Board: 
    def __init__(self, app):
        self.app = app
    def draw(self, app):
        drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
             fill = "yellow")
    
class StoreA:
    def __init__(self, app):
        self.app = app
    def draw(self, app):
        drawRect(app.storeALeft, app.storeATop, app.storeAWidth, app.storeAHeight,
             fill = "green" )
    def drawMarbles(self, app):
        marblesCount = len(app.storeAMarbles)
        drawLabel(f"{marblesCount}", (app.storeALeft - 10), 
                  (app.storeATop +(app.storeAHeight/2)), align="center")
        for cxMarble, cyMarble in app.storeAMarbles:
             drawCircle(cxMarble, cyMarble, app.radiusMarble, fill = "pink")



class StoreB:
    def __init__(self, app):
        self.app = app
    def draw(self, app):
        drawRect(app.storeBLeft, app.storeBTop, app.storeBWidth, app.storeBHeight,
             fill = "green" )
    def drawMarbles(self, app):
        marblesCount = len(app.storeBMarbles)
        drawLabel(f"{marblesCount}", (app.storeBLeft + app.storeBWidth + 10), 
                  (app.storeBTop +(app.storeBHeight/2)), align="center")
        for cxMarble, cyMarble in app.storeBMarbles:
             drawCircle(cxMarble, cyMarble, app.radiusMarble, fill = "pink")

class PitsA: 
    def __init__(self, app):
        self.app = app
        
    def draw(self, app):
        for cx, cy in app.circlesA:
            drawCircle(cx, cy, app.pitRadius-3, fill = "blue")
    
    def drawMarbles(self, app):
        for pitAndMarbles in app.marblesA:
            cx, cy = pitAndMarbles[0]
            marblesCount = len(pitAndMarbles[1])
            drawLabel(f"{marblesCount}", cx, cy-app.pitRadius-5, align="center")
            for cxMarble, cyMarble in pitAndMarbles[1]:
                drawCircle(cxMarble, cyMarble, app.radiusMarble, fill = "pink")

class PitsB:
    def __init__(self, app):
        self.app = app
        
        
    def draw(self, app):
        for cx, cy in app.circlesB:
            drawCircle(cx, cy, app.pitRadius-3, fill = "blue")
    
    def drawMarbles(self, app):
        for pitAndMarbles in app.marblesB:
            cx, cy = pitAndMarbles[0]
            marblesCount = len(pitAndMarbles[1])
            drawLabel(f"{marblesCount}", cx, cy+app.pitRadius+5, align="center")
            for cxMarble, cyMarble in pitAndMarbles[1]:
                drawCircle(cxMarble, cyMarble, app.radiusMarble, fill = "pink")




class PlayerA:
    def __init__(self, app):
        self.app = app
    # def hoverPit(self): #to change color of pit 
    #     pass
    def drawTurn(self, app):
        pass

    def moveMarblesInpit(self, app, cxTarget, cyTarget):
        indexTarget = PlayerA.getIndexCircleTarget(app, cxTarget, cyTarget)
        numMarbles = len(app.marblesA[indexTarget][1])
        nextCircle = indexTarget
        oppCircle = 5
        while numMarbles != 0:
            nextCircle += 1
            #deposit marble in my own pit 
            if nextCircle < 6:
                cxPit, cyPit = app.marblesA[nextCircle][0]
                cxMarble, cyMarble = PlayerA.getRangeMarbleInCircle(app, cxPit, cyPit)
                app.marblesA[nextCircle][1].append((cxMarble, cyMarble))
                app.marblesA[indexTarget][1].pop(0)
                numMarbles -= 1
            #deposit marble in store 
            elif nextCircle == 6:
                cxMarble, cyMarble = PlayerA.getRangeMarbleInRect(app)
                app.storeAMarbles.append((cxMarble, cyMarble))
                app.marblesA[indexTarget][1].pop(0)
                numMarbles -= 1
            #deposit marble in opponent pit
            elif nextCircle > 6 and oppCircle >= 0:
                cxPit, cyPit = app.marblesB[oppCircle][0]
                cxMarble, cyMarble = PlayerA.getRangeMarbleInCircle(app,cxPit, cyPit)
                app.marblesB[oppCircle][1].append((cxMarble, cyMarble))
                app.marblesA[indexTarget][1].pop(0)
                numMarbles -= 1
                oppCircle -= 1
            #made a turn of the whole board and have to deposit in my board again
            #case if I have a lot of marbles in chosen pit 
            else:
                nextCircle = -1
        app.playerATurn = False
        app.playerBTurn = True 
        #if last marble lands in store, take another turn 
        if nextCircle == 6:
            app.messageTurn = "Your Turn again"
            app.playerATurn = True 
            app.playerBTurn = False 

        #if last marble lands in my own pit and its empty
        if nextCircle >= 0 and nextCircle < 6:
            if len(app.marblesA[nextCircle][1]) == 1:
                # capture that last marble 
                app.marblesA[nextCircle][1] = []
                cxMarble, cyMarble = PlayerA.getRangeMarbleInRect(app)
                app.storeAMarbles.append((cxMarble, cyMarble))
                # capture all the marble in opposite pit of the opponent 
                if len(app.marblesB[nextCircle][1]) != []:
                    capturedMarbles = len(app.marblesB[nextCircle][1])
                    app.marblesB[nextCircle][1] = []
                    for i in range (capturedMarbles):
                        cxMarble, cyMarble = PlayerA.getRangeMarbleInRect(app)
                        app.storeAMarbles.append((cxMarble, cyMarble))

    @staticmethod
    def getIndexCircleTarget(app, cxTarget, cyTarget):
        for i in range (6):
            if app.marblesA[i][0] == (cxTarget, cyTarget):
                return i 
            
    def getRangeMarbleInCircle(app, cxPit, cyPit):
        cxMarble = random.uniform((cxPit - app.pitRadius + app.radiusMarble + 10),(
            cxPit + app.pitRadius - app.radiusMarble - 10))
        cyMarble = random.uniform((cyPit - app.pitRadius + app.radiusMarble + 10),(
            cyPit + app.pitRadius - app.radiusMarble - 10))
        return (cxMarble, cyMarble)
    
    def getRangeMarbleInRect(app):
        cxMarble = random.uniform((app.storeALeft + app.radiusMarble), (app.storeALeft+
                                app.storeAWidth - app.radiusMarble))
        cyMarble = random.uniform((app.storeATop + app.radiusMarble), (app.storeATop+
                                app.storeAHeight - app.radiusMarble))
        return (cxMarble, cyMarble)


class PlayerB:
    def __init__(self, app):
        self.app = app
    # def hoverPit(self): #to change color of pit 
    #     pass
    def drawTurn(self, app):
        pass

    def moveMarblesInpit(self, app, cxTarget, cyTarget):
        indexTarget = PlayerB.getIndexCircleTarget(app, cxTarget, cyTarget)
        numMarbles = len(app.marblesB[indexTarget][1])
        nextCircle = indexTarget
        oppCircle = 0
        while numMarbles != 0:
            nextCircle -= 1
            #deposit marble in my own pit 
            if nextCircle < 6 and nextCircle >= 0:
                cxPit, cyPit = app.marblesB[nextCircle][0]
                cxMarble, cyMarble = PlayerB.getRangeMarbleInCircle(app, cxPit, cyPit)
                app.marblesB[nextCircle][1].append((cxMarble, cyMarble))
                app.marblesB[indexTarget][1].pop(0)
                numMarbles -= 1
            #deposit marble in store 
            elif nextCircle == -1:
                cxMarble, cyMarble = PlayerB.getRangeMarbleInRect(app)
                app.storeBMarbles.append((cxMarble, cyMarble))
                app.marblesB[indexTarget][1].pop(0)
                numMarbles -= 1
            #deposit marble in opponent pit
            elif nextCircle < -1 and oppCircle >= 0 and oppCircle < 6:
                cxPit, cyPit = app.marblesA[oppCircle][0]
                cxMarble, cyMarble = PlayerB.getRangeMarbleInCircle(app,cxPit, cyPit)
                app.marblesA[oppCircle][1].append((cxMarble, cyMarble))
                app.marblesB[indexTarget][1].pop(0)
                numMarbles -= 1
                oppCircle += 1
            #made a turn of the whole board and have to deposit in my board again
            #case if I have a lot of marbles in chosen pit 
            else:
                nextCircle = 5
        app.playerBTurn = False
        app.playerATurn = True 
        #if last marble lands in store, take another turn 
        if nextCircle == -1:
            app.messageTurn = "Your Turn again"
            app.playerBTurn = True
            app.playerATurn = False

        #if last marble lands in my own pit and its empty
        if nextCircle >= 0 and nextCircle < 6:
            if len(app.marblesB[nextCircle][1]) == 1:
                # capture that last marble 
                app.marblesB[nextCircle][1] = []
                cxMarble, cyMarble = PlayerB.getRangeMarbleInRect(app)
                app.storeBMarbles.append((cxMarble, cyMarble))
                # capture all the marble in opposite pit of the opponent 
                if len(app.marblesA[nextCircle][1]) != []:
                    capturedMarbles = len(app.marblesB[nextCircle][1])
                    app.marblesA[nextCircle][1] = []
                    for i in range (capturedMarbles):
                        cxMarble, cyMarble = PlayerB.getRangeMarbleInRect(app)
                        app.storeBMarbles.append((cxMarble, cyMarble))

    @staticmethod
    def getIndexCircleTarget(app, cxTarget, cyTarget):
        for i in range (6):
            if app.marblesB[i][0] == (cxTarget, cyTarget):
                return i 
            
    def getRangeMarbleInCircle(app, cxPit, cyPit):
        cxMarble = random.uniform((cxPit - app.pitRadius + app.radiusMarble + 10),(
            cxPit + app.pitRadius - app.radiusMarble - 10))
        cyMarble = random.uniform((cyPit - app.pitRadius + app.radiusMarble + 10),(
            cyPit + app.pitRadius - app.radiusMarble - 10))
        return (cxMarble, cyMarble)
    
    def getRangeMarbleInRect(app):
        cxMarble = random.uniform((app.storeBLeft + app.radiusMarble), (app.storeBLeft+
                                app.storeBWidth - app.radiusMarble))
        cyMarble = random.uniform((app.storeBTop + app.radiusMarble), (app.storeBTop+
                                app.storeBHeight - app.radiusMarble))
        return (cxMarble, cyMarble)




################################################################################
def onAppStart(app):
    app.boardWidth = (app.width * 3) / 4
    app.boardHeight = (app.height * 2) / 4
    app.boardLeft = app.width/2 - app.boardWidth/2
    app.boardTop = app.height/2 - app.boardHeight/2
  

    app.pitRadius = 30
    app.spaceWidthPitStore = (app.boardWidth) / 8 
    app.spaceHeightPit = (app.boardHeight) / 3 
   
    app.storeBWidth = (app.spaceWidthPitStore * 3)/4
    app.storeBHeight = (app.boardHeight * 2)/4
    app.storeBLeft = (app.spaceWidthPitStore/2 -  app.storeBWidth/2) + app.boardLeft
    app.storeBTop = (app.boardHeight/2 - app.storeBHeight/2) +  app.boardTop
    app.storeBMarbles = []

    app.storeAWidth = (app.spaceWidthPitStore * 3)/4
    app.storeAHeight = (app.boardHeight * 2)/4
    app.storeALeft = (app.spaceWidthPitStore/2 -  app.storeAWidth/2) + app.boardLeft + app.spaceWidthPitStore*7
    app.storeATop = (app.boardHeight/2 - app.storeAHeight/2) +  app.boardTop
    app.storeAMarbles = []


    app.circlesA = []
    for numPits in range(6):
            cx = app.boardLeft + app.spaceWidthPitStore * (numPits+1) + (app.pitRadius)
            cy = app.boardTop + (app.spaceHeightPit * 2) + app.pitRadius + 55
            app.circlesA.append((cx, cy)) 

    app.marblesA = []
    for cx, cy in app.circlesA:
        app.marblesA.append([(cx, cy), [(cx, cy-7), (cx, cy+7), 
                                 (cx-7, cy), (cx+7, cy)]])
        

    app.circlesB = []
    for numPits in range(6):
            cx = app.boardLeft + app.spaceWidthPitStore * (numPits+1) + (app.pitRadius)
            cy = app.boardTop + app.pitRadius + 17
            app.circlesB.append((cx, cy)) 


    app.marblesB = []
    for cx, cy in app.circlesB:
        app.marblesB.append([(cx, cy), [(cx, cy-7), (cx, cy+7), 
                                 (cx-7, cy), (cx+7, cy)]])

    app.radiusMarble = 3

    app.playerATurn = True 
    app.playerBTurn = False
    app.messageTurn = "Your Turn"

    

board = Board(app) 
storeA = StoreA(app)  
storeB = StoreB(app)
pitsA = PitsA(app)
pitsB = PitsB(app)
playerA = PlayerA(app)
playerB = PlayerB(app)
objects = [board, storeA, storeB, pitsA, pitsB]
objectsWithMarbles  = [storeA, storeB, pitsA, pitsB]

def redrawAll(app):
    for obj in objects:
        obj.draw(app)
    # for obj in objectsWithMarbles:
    #     obj.drawMarbles(app)
    pitsA.drawMarbles(app)
    pitsB.drawMarbles(app)
    storeA.drawMarbles(app)
    storeB.drawMarbles(app)
    # print(app.marblesA) 


# def onMouseMove(app, mouseX, mouseY):
#     pass

def onMousePress(app, mouseX, mouseY):
    for cx, cy in app.circlesA:
        if distance(cx, cy, mouseX, mouseY) <= app.pitRadius:
            if app.playerATurn and (not app.playerBTurn):
                moveMarblesInPitA(app, cx, cy)
                

    #opponent's turn 
    for cx, cy in app.circlesB:
        if distance(cx, cy, mouseX, mouseY) <= app.pitRadius:
            if app.playerBTurn and (not app.playerATurn):
                moveMarblesInPitB(app, cx, cy)
                


def moveMarblesInPitA(app, cxTarget, cyTarget):
    playerA.moveMarblesInpit(app, cxTarget, cyTarget)

def moveMarblesInPitB(app, cxTarget, cyTarget):
    playerB.moveMarblesInpit(app, cxTarget, cyTarget)

def main():
    runApp(width = 800, height = 800)

if __name__ == '__main__':
    main()





##problems 

#Your turn mesasge 
#gameOver 
#is Winner 





#notes 
#deposit marble in my own pit 
    #deposit marble in store 
    #deposit marble in opponent pit
    #if last marble lands in store, take another turn 
    #if last marble lands in my own pit and its empty, 
            # capture that last marble 
            # capture all the marble in opposite pit of the opponent 
