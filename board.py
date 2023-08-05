###Mancala112 by Fatou Gueye###
from cmu_graphics import *
import random

class Board: 
    def __init__(self, app):
        self.app = app
    def draw(self, app):
        drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
             fill = "yellow")
    def drawBoardMessage(self, app):
        drawLabel(app.gameOverMessage, app.width/2, 
                      app.boardTop - 30, align = "center", fill = "red", bold = True)
    def checkWinner(self, app):
        if app.gameOver:
            if len(app.storeAMarbles) > len(app.storeBMarbles):
                winner = app.playerAName
                loser = app.playerBName
                drawLabel(f"{winner} IS THE WINNER!", app.width/2, 30, fill = "gold")
                drawLabel(f"{winner} : {len(app.storeAMarbles)} points", app.width/2, 60)
                drawLabel(f"{loser} : {len(app.storeBMarbles)} points", app.width/2, 80)

            elif len(app.storeBMarbles) > len(app.storeAMarbles):
                winner = app.playerBName
                loser = app.playerAName
                drawLabel(f"{winner} IS THE WINNER!", app.width/2, 30, fill = "gold")
                drawLabel(f"{winner} : {len(app.storeBMarbles)} points", app.width/2, 60)
                drawLabel(f"{loser} : {len(app.storeAMarbles)} points", app.width/2, 80)

            else:
                drawLabel(f"IT'S A TIE!", app.width/2, 30, fill = "gold")
                drawLabel(f"{app.playerAName} : {len(app.storeAMarbles)} points", app.width/2, 60)
                drawLabel(f"{app.playerBName} : {len(app.storeBMarbles)} points", app.width/2, 80)
                
    # def drawWinnerMessage(self, app):
    #     playerWinner = 
    #     if 
    
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
        self.allEmpty = False
        
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
    
    # def allEmpty(self, app):
    #     for circleCheck in app.marblesA:
    #         if circleCheck[1] != []:
    #             return False
    #     return True 

class PitsB:
    def __init__(self, app):
        self.app = app
        #self.allEmpty = False
        
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
    
    # def allEmpty(self, app):
    #     for circleCheck in app.marblesB:
    #         if circleCheck[1] != []:
    #             return False
    #     return True 




class PlayerA:
    def __init__(self, app):
        self.app = app
   
    def moveMarblesInpit(self, app, cxTarget, cyTarget):
        app.messageTurnA = f"{app.playerAName}'s Turn"
        indexTarget = PlayerA.getIndexCircleTarget(app, cxTarget, cyTarget)
        numMarbles = len(app.marblesA[indexTarget][1])
        if app.marblesA[indexTarget][1] != []:
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
                    # playerA.moveMarblesInpit(app, cxTarget, cyTarget)
                    nextCircle = -1
            app.playerATurn = False
            app.playerBTurn = True 
            #if last marble lands in store, take another turn 
            if nextCircle == 6:
                app.messageTurnA = f"{app.playerAName}'s Turn again"
                app.playerATurn = True 
                app.playerBTurn = False 

            #if last marble lands in my own pit and its empty
            elif nextCircle >= 0 and nextCircle < 6:
                if (len(app.marblesA[nextCircle][1]) == 1) and (len(app.marblesB[nextCircle][1]) >0):
                    # capture that last marble 
                    app.marblesA[nextCircle][1] = []
                    cxMarble, cyMarble = PlayerA.getRangeMarbleInRect(app)
                    app.storeAMarbles.append((cxMarble, cyMarble))
                    # capture all the marble in opposite pit of the opponent 
                   
                    capturedMarbles = len(app.marblesB[nextCircle][1])
                    app.marblesB[nextCircle][1] = []
                    for i in range (capturedMarbles):
                        cxMarble, cyMarble = PlayerA.getRangeMarbleInRect(app)
                        app.storeAMarbles.append((cxMarble, cyMarble))
            # app.messageTurnA = f"{app.playerAName}'s Turn"

    def drawMessageTurnA(self, app):
        drawLabel(app.messageTurnA, (app.boardLeft + app.boardWidth - 30), 
                  (app.boardTop + app.boardHeight + 30), fill = "black", align = "center" )

    def captureAllRestMarbles(self, app):
        marblesLeftA = 0
        for pit in app.marblesA:
            marblesLeftA += len(pit[1])
            pit[1] = []
        if marblesLeftA > 0:
            for i in range (marblesLeftA):
                cxMarble, cyMarble = PlayerA.getRangeMarbleInRect(app)
                app.storeAMarbles.append((cxMarble, cyMarble))

    @staticmethod
    def getIndexCircleTarget(app, cxTarget, cyTarget):
        for i in range (6):
            if app.marblesA[i][0] == (cxTarget, cyTarget):
                return i 
            
    @staticmethod         
    def getRangeMarbleInCircle(app, cxPit, cyPit):
        cxMarble = random.uniform((cxPit - app.pitRadius + app.radiusMarble + 10),(
            cxPit + app.pitRadius - app.radiusMarble - 10))
        cyMarble = random.uniform((cyPit - app.pitRadius + app.radiusMarble + 10),(
            cyPit + app.pitRadius - app.radiusMarble - 10))
        return (cxMarble, cyMarble)
    
    @staticmethod
    def getRangeMarbleInRect(app):
        cxMarble = random.uniform((app.storeALeft + app.radiusMarble), (app.storeALeft+
                                app.storeAWidth - app.radiusMarble))
        cyMarble = random.uniform((app.storeATop + app.radiusMarble), (app.storeATop+
                                app.storeAHeight - app.radiusMarble))
        return (cxMarble, cyMarble)


class PlayerB:
    def __init__(self, app):
        self.app = app
    
    def moveMarblesInpit(self, app, cxTarget, cyTarget):
        app.messageTurnB = f"{app.playerBName}'s Turn"
        indexTarget = PlayerB.getIndexCircleTarget(app, cxTarget, cyTarget)
        numMarbles = len(app.marblesB[indexTarget][1])
        if app.marblesB[indexTarget][1] != []:
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
                    nextCircle = 6
            app.playerBTurn = False
            app.playerATurn = True 
            #if last marble lands in store, take another turn 
            if nextCircle == -1:
                app.messageTurnB = f"{app.playerBName}'s Turn again"
                app.playerBTurn = True
                app.playerATurn = False

            elif nextCircle >= 0 and nextCircle < 6:
                if (len(app.marblesB[nextCircle][1]) == 1) and (len(app.marblesA[nextCircle][1]) >0):
                    # capture that last marble 
                    app.marblesB[nextCircle][1] = []
                    cxMarble, cyMarble = PlayerB.getRangeMarbleInRect(app)
                    app.storeBMarbles.append((cxMarble, cyMarble))
                    # capture all the marble in opposite pit of the opponent 
                    capturedMarbles = len(app.marblesA[nextCircle][1])
                    app.marblesA[nextCircle][1] = []
                    for i in range (capturedMarbles):
                        cxMarble, cyMarble = PlayerB.getRangeMarbleInRect(app)
                        app.storeBMarbles.append((cxMarble, cyMarble))
        
    def drawMessageTurnB(self, app):
        drawLabel(app.messageTurnB, (app.boardLeft + app.boardWidth - 30), 
                  (app.boardTop - 30), fill = "black", align = "center" )
    
    def captureAllRestMarbles(self, app):
        marblesLeftB = 0
        for pit in app.marblesB:
            marblesLeftB += len(pit[1])
            pit[1] = []
        if marblesLeftB > 0:
            for i in range (marblesLeftB):
                cxMarble, cyMarble = PlayerB.getRangeMarbleInRect(app)
                app.storeBMarbles.append((cxMarble, cyMarble))

    @staticmethod
    def getIndexCircleTarget(app, cxTarget, cyTarget):
        for i in range (6):
            if app.marblesB[i][0] == (cxTarget, cyTarget):
                return i 
            
    @staticmethod        
    def getRangeMarbleInCircle(app, cxPit, cyPit):
        cxMarble = random.uniform((cxPit - app.pitRadius + app.radiusMarble + 10),(
            cxPit + app.pitRadius - app.radiusMarble - 10))
        cyMarble = random.uniform((cyPit - app.pitRadius + app.radiusMarble + 10),(
            cyPit + app.pitRadius - app.radiusMarble - 10))
        return (cxMarble, cyMarble)
    
    @staticmethod
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


    app.playerAName = input("Player A Name")
    app.playerBName = input("Player B Name")
    app.messageTurnA = f"{app.playerAName}'s Turn"
    app.messageTurnB = f"{app.playerBName}'s Turn"

    app.gameOver = False 
    app.gameOverMessage = "GAME IS OVER"


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
    if app.playerATurn and (not app.playerBTurn):
        playerA.drawMessageTurnA(app)

    if app.playerBTurn and (not app.playerATurn):
        playerB.drawMessageTurnB(app)
    if app.gameOver:
        board.drawBoardMessage(app)
        board.checkWinner(app)
        #printing winner, will make it prettier after



# def onMouseMove(app, mouseX, mouseY):
#     pass

def onMousePress(app, mouseX, mouseY):
    if not app.gameOver:
        for cx, cy in app.circlesA:
            if distance(cx, cy, mouseX, mouseY) <= app.pitRadius:
                if app.playerATurn and (not app.playerBTurn):
                    moveMarblesInPitA(app, cx, cy)
                    

        #opponent's turn 
        for cx, cy in app.circlesB:
            if distance(cx, cy, mouseX, mouseY) <= app.pitRadius:
                if app.playerBTurn and (not app.playerATurn):
                    moveMarblesInPitB(app, cx, cy)   
    

    # if pitsA.allEmpty(app)==True or pitsB.allEmpty(app)==True:
    if allEmptyA(app) or allEmptyB(app):
        app.gameOver = True
    
    if app.gameOver:
        playerB.captureAllRestMarbles(app)
        playerA.captureAllRestMarbles(app) 
        app.playerATurn = False 
        app.playerBTurn = False
        return 
        


def moveMarblesInPitA(app, cxTarget, cyTarget):
    # app.messageTurnA = f"{app.playerAName}'s Turn"
    indexTarget = PlayerA.getIndexCircleTarget(app, cxTarget, cyTarget)
    if (app.marblesA[indexTarget][1]) != []:
        playerA.moveMarblesInpit(app, cxTarget, cyTarget)
    

def moveMarblesInPitB(app, cxTarget, cyTarget):
    indexTarget = PlayerB.getIndexCircleTarget(app, cxTarget, cyTarget)
    if (app.marblesB[indexTarget][1]) != []:
        playerB.moveMarblesInpit(app, cxTarget, cyTarget)

def getIndexCircleTarget(app, cxTarget, cyTarget):
        for i in range (6):
            if app.marblesB[i][0] == (cxTarget, cyTarget):
                return i 

def allEmptyA(app):
        for circleCheck in app.marblesA:
            if len(circleCheck[1]) > 0:
                return False
        return True 

def allEmptyB(app):
        for circleCheck in app.marblesB:
            if len(circleCheck[1]) > 0:
                return False
        return True 

# def checkGameOver(app):
#     if allEmptyA(app) or allEmptyB(app):

#     # if pitsA.allEmpty or pitsB.allEmpty:
#         app.gameOver = True
    
#         playerB.captureAllRestMarbles(app)
        

#         playerA.captureAllRestMarbles(app) 
#         app.playerATurn = False 
#         app.playerBTurn = False

def main():
    runApp(width = 800, height = 800)

if __name__ == '__main__':
    main() 





##problems 
#problem with capture all rest marbles
#have problem when its going on all over the board when you have lots of marbles
#when it has to come back to its house again 
#also does not gameOver 

#gameOver 
     # if all the pits in one of the side are empty 
     #other player capture all the marbles remaining in his pits 
#is Winner 
     #which store has the most marbles 
#minimax 
# def hoverPit(self): #to change color of pit 




#notes 
#deposit marble in my own pit 
    #deposit marble in store 
    #deposit marble in opponent pit
    #if last marble lands in store, take another turn 
    #if last marble lands in my own pit and its empty, 
            # capture that last marble 
            # capture all the marble in opposite pit of the opponent 
