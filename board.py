###Mancala112 by Fatou Gueye###
from cmu_graphics import *
import random
import copy

class Board: 
    def __init__(self, app):
        self.app = app

    def draw(self, app):
        drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
             fill = "yellow")
        
    def drawBoardMessage(self, app):
        drawLabel(app.gameOverMessage, app.width/2, 
                      app.boardTop - 30, align = "center", fill = "red", 
                      bold = True)
        
    def checkWinner(self, app):
        if app.gameOver:
            if len(app.storeAMarbles) > len(app.storeBMarbles):
                winner = app.playerAName
                loser = app.playerBName
                drawLabel(f"{winner} IS THE WINNER!", app.width/2, 30, 
                          fill = "green")
                drawLabel(f"{winner} : {len(app.storeAMarbles)} points", 
                          app.width/2, 60)
                drawLabel(f"{loser} : {len(app.storeBMarbles)} points", 
                          app.width/2, 80)

            elif len(app.storeBMarbles) > len(app.storeAMarbles):
                winner = app.playerBName
                loser = app.playerAName
                drawLabel(f"{winner} IS THE WINNER!", app.width/2, 30,
                           fill = "green")
                drawLabel(f"{winner} : {len(app.storeBMarbles)} points", 
                          app.width/2, 60)
                drawLabel(f"{loser} : {len(app.storeAMarbles)} points", 
                          app.width/2, 80)

            else:
                drawLabel(f"IT'S A TIE!", app.width/2, 30, fill = "green")
                drawLabel(f"{app.playerAName} : {len(app.storeAMarbles)} points",
                          app.width/2, 60)
                drawLabel(f"{app.playerBName} : {len(app.storeBMarbles)} points", 
                          app.width/2, 80)

    # get the present state of my board for my AI
    @staticmethod
    def getBoardState(app):
        boardState = []
        for circle in app.marblesA:
            boardState.append(len(circle[1]))
        boardState.append(len(app.storeAMarbles))
        rightToLeftB = []
        for circle in app.marblesB:
            rightToLeftB.append(len(circle[1]))
        boardState.extend(rightToLeftB[::-1])
        boardState.append(len(app.storeBMarbles))
        boardState.append(app.playerATurn)
        print("boardState", boardState)
        return boardState 
    
# class Name:



    
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
                if ((len(app.marblesA[nextCircle][1]) == 1) and 
                (len(app.marblesB[nextCircle][1]) >0)):
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
                  (app.boardTop + app.boardHeight + 30), fill = "black",
                    align = "center" )

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
        cxMarble = (random.uniform((cxPit - app.pitRadius + app.radiusMarble + 10),(
            cxPit + app.pitRadius - app.radiusMarble - 10)))
        cyMarble = (random.uniform((cyPit - app.pitRadius + app.radiusMarble + 10),(
            cyPit + app.pitRadius - app.radiusMarble - 10)))
        return (cxMarble, cyMarble)
    
    @staticmethod
    def getRangeMarbleInRect(app):
        cxMarble = (random.uniform((app.storeALeft + app.radiusMarble),
                         (app.storeALeft+app.storeAWidth - app.radiusMarble)))
        cyMarble = (random.uniform((app.storeATop + app.radiusMarble),
                        (app.storeATop+app.storeAHeight - app.radiusMarble)))
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
                if ((len(app.marblesB[nextCircle][1]) == 1) and
                (len(app.marblesA[nextCircle][1]) >0)):
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
        cxMarble =(random.uniform((cxPit - app.pitRadius + app.radiusMarble + 10)
                            ,(cxPit + app.pitRadius - app.radiusMarble - 10)))
        cyMarble =(random.uniform((cyPit - app.pitRadius + app.radiusMarble + 10)
                            ,(cyPit + app.pitRadius - app.radiusMarble - 10)))
        return (cxMarble, cyMarble)
    
    @staticmethod
    def getRangeMarbleInRect(app):
        cxMarble = (random.uniform((app.storeBLeft + app.radiusMarble),
                         (app.storeBLeft+app.storeBWidth - app.radiusMarble)))
        cyMarble = (random.uniform((app.storeBTop + app.radiusMarble),
                         (app.storeBTop+app.storeBHeight - app.radiusMarble)))
        return (cxMarble, cyMarble)
    
##temporary putting player AI in this file 
class PlayerAI:
    def __init__(self, app, depth, state, maximizing):
        self.app = app
        self.depth = depth
        self.state = state 
        self.maximizing = maximizing

    #when ai move the marbles: get the best move on minimax algo and make that move 
    def moveMarblesInPit(self, app):
        bestMove, bestScore = PlayerAI.minimax(self.state, self.depth, self.maximizing)
        print("bestMove",bestMove)
        app.messageTurnB = f"Computer's Turn"
        indexTarget = 5 - (bestMove - 7)
        numMarbles = len(app.marblesB[indexTarget][1])
        if app.marblesB[indexTarget][1] != []:
            nextCircle = indexTarget
            oppCircle = 0
            while numMarbles != 0:
                nextCircle -= 1
                #deposit marble in my own pit 
                if nextCircle < 6 and nextCircle >= 0:
                    cxPit, cyPit = app.marblesB[nextCircle][0]
                    cxMarble, cyMarble = PlayerAI.getRangeMarbleInCircle(app, cxPit, cyPit)
                    app.marblesB[nextCircle][1].append((cxMarble, cyMarble))
                    app.marblesB[indexTarget][1].pop(0)
                    numMarbles -= 1
                #deposit marble in store 
                elif nextCircle == -1:
                    cxMarble, cyMarble = PlayerAI.getRangeMarbleInRect(app)
                    app.storeBMarbles.append((cxMarble, cyMarble))
                    app.marblesB[indexTarget][1].pop(0)
                    numMarbles -= 1
                #deposit marble in opponent pit
                elif nextCircle < -1 and oppCircle >= 0 and oppCircle < 6:
                    cxPit, cyPit = app.marblesA[oppCircle][0]
                    cxMarble, cyMarble = PlayerAI.getRangeMarbleInCircle(app,cxPit, cyPit)
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
                app.messageTurnB = f"Computers's Turn again"
                app.playerBTurn = True
                app.playerATurn = False

            elif nextCircle >= 0 and nextCircle < 6:
                if ((len(app.marblesB[nextCircle][1]) == 1) and 
                    (len(app.marblesA[nextCircle][1]) >0)):
                    # capture that last marble 
                    app.marblesB[nextCircle][1] = []
                    cxMarble, cyMarble = PlayerAI.getRangeMarbleInRect(app)
                    app.storeBMarbles.append((cxMarble, cyMarble))
                    # capture all the marble in opposite pit of the opponent 
                    capturedMarbles = len(app.marblesA[nextCircle][1])
                    app.marblesA[nextCircle][1] = []
                    for i in range (capturedMarbles):
                        cxMarble, cyMarble = PlayerAI.getRangeMarbleInRect(app)
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
                cxMarble, cyMarble = PlayerAI.getRangeMarbleInRect(app)
                app.storeBMarbles.append((cxMarble, cyMarble))

    @staticmethod
    def minimax(state, depth, maximizing):
        # print("state",state)
        print("depth",depth)
        if (depth <= 0) or (PlayerAI.gameOver(state)==True):
            # print("aaaaaa")
            return (None, PlayerAI.getScore(state))
        else:
            if maximizing:
                bestScore = -10000
                bestMove = None
                possibleMoves = PlayerAI.getPossibleMoves(state)
                for move in possibleMoves:
                    newState = PlayerAI.getNewState(move, state)
                    # depth -= 1
                    # maximizing = False
                    _, score = PlayerAI.minimax(newState, depth-1, not maximizing)
                    # print("score", score)
                    #arrive at a new state 
                    #recurse with that new state 
                    #after caluculation 
                    #get back to the original state 
                    if score > bestScore:
                        bestScore = score 
                        bestMove = move 
                return (bestMove, bestScore)
            else:
                bestScore = +10000
                bestMove = None
                possibleMoves = PlayerAI.getPossibleMoves(state)
                for move in possibleMoves:
                    newState = PlayerAI.getNewState(move, state)
                    # depth -= 1
                    # maximizing = True
                    _, score = PlayerAI.minimax(newState, depth-1, not maximizing)
                    if score < bestScore:
                        bestScore = score 
                        bestMove = move 
                return (bestMove, bestScore)

            
    @staticmethod        
    def getRangeMarbleInCircle(app, cxPit, cyPit):
        cxMarble =(random.uniform((cxPit - app.pitRadius + app.radiusMarble + 10)
                            ,(cxPit + app.pitRadius - app.radiusMarble - 10)))
        cyMarble =(random.uniform((cyPit - app.pitRadius + app.radiusMarble + 10)
                            ,(cyPit + app.pitRadius - app.radiusMarble - 10)))
        return (cxMarble, cyMarble)
    
    @staticmethod
    def getRangeMarbleInRect(app):
        cxMarble = (random.uniform((app.storeBLeft + app.radiusMarble),
                         (app.storeBLeft+app.storeBWidth - app.radiusMarble)))
        cyMarble = (random.uniform((app.storeBTop + app.radiusMarble),
                         (app.storeBTop+app.storeBHeight - app.radiusMarble)))
        return (cxMarble, cyMarble)
    #helper function for my minimax 
    @staticmethod
    def getPossibleMoves(state):
        possibleMoves = []
        if state[-1] == True:
            for pitNum in range(6):
                if state[pitNum] > 0:
                    possibleMoves.append(pitNum)
        else:
            for pitNum in range(7, 13):
                if state[pitNum] > 0:
                    possibleMoves.append(pitNum)
        print("possibleMoves",possibleMoves)
        return possibleMoves
    #helper function for my minimax 
    @staticmethod
    def getNewState(move, state):
        newState = (state).copy()
        newState[-1] = not newState[-1]
        if move >= 0 and move < 6:
            numMarbles = state[move]
            nextPit = move
            newState[move] = 0
            oppCircle = 7
            while numMarbles != 0:
                nextPit += 1
                if nextPit <= 6:
                    newState[nextPit] += 1
                    numMarbles -= 1
                elif nextPit > 6 and oppCircle < 13:
                    newState[oppCircle] += 1
                    numMarbles -= 1
                    oppCircle += 1
                else:
                    oppCircle = 7
                    nextPit = -1 
        elif move > 6 and move < 13:
            numMarbles = state[move]
            nextPit = move
            newState[move] = 0
            oppCircle = 0
            while numMarbles != 0:
                nextPit += 1
                if nextPit > 6 and nextPit <= 13:
                    newState[nextPit] += 1
                    numMarbles -= 1
                elif nextPit > 13 and oppCircle < 6:
                    newState[oppCircle] += 1
                    numMarbles -= 1
                    oppCircle += 1
                else:
                    oppCircle = 0
                    nextPit = 6
       
        return newState 
        # self.state = newState 
        # return self.state 
    #helper function for minimax
    @staticmethod
    def gameOver(state):
        if ((sum(state[:6])) == 0) or ((sum(state[7:13])) == 0):
            return True 
        return False 
    #heuristic function for minimax 
    @staticmethod
    def getScore(state):
        playerAmarbles = state[6]
        playerBmarbles = state[13]
        if state[-1] == True:
            return playerAmarbles - playerBmarbles  + 10
        else:
            return playerBmarbles - playerAmarbles + 7
        
class Button:
    def __init__(self, left, top, width, height, text, color, function):
        self.left = left
        self.top = top
        self.width = width 
        self.height = height 
        self.text = text
        self.color = color
        self.colorref= color
        self.function = function

    
    def draw(self):
        drawRect(self.left, self.top, self.width, self.height, fill = self.color)
        drawLabel(self.text, self.left+(self.width/2), self.top+(self.height/2), 
                  size=10, fill = "black", bold = True, align = "center")
        
    def checkForPress(self, app, mX, mY):
        if ((self.left<=mX<(self.left + self.width)) and 
            (self.top<=mY<(self.top + self.height))):
            self.function(app)
    
    def hoverColor(self, app, mX, mY):
        if ((self.left<=mX<(self.left + self.width)) and 
            (self.top<=mY<(self.top + self.height))):
            self.color = "olivedrab"
        else:
            self.color = self.colorref
  

################################################################################
def onAppStart(app):
    app.board = Board(app) 
    app.storeA = StoreA(app)  
    app.storeB = StoreB(app)
    app.pitsA = PitsA(app)
    app.pitsB = PitsB(app)
    app.playerA = PlayerA(app)
    app.playerB = PlayerB(app)
    app.objects = [app.board, app.storeA, app.storeB, app.pitsA, app.pitsB]
    #to change play modes for now 
    app.playerVSplayer = None
    app.playerVScomputer = None

    app.boardWidth = (app.width * 3) / 4
    app.boardHeight = (app.height * 2) / 4
    app.boardLeft = app.width/2 - app.boardWidth/2
    app.boardTop = app.height/2 - app.boardHeight/2
  

    app.pitRadius = 30
    app.spaceWidthPitStore = (app.boardWidth) / 8 
    app.spaceHeightPit = (app.boardHeight) / 3 
   
    app.storeBWidth = (app.spaceWidthPitStore * 3)/4
    app.storeBHeight = (app.boardHeight * 2)/4
    app.storeBLeft = ((app.spaceWidthPitStore/2 -  app.storeBWidth/2)
    + app.boardLeft)
    app.storeBTop = (app.boardHeight/2 - app.storeBHeight/2) +  app.boardTop
    app.storeBMarbles = []

    app.storeAWidth = (app.spaceWidthPitStore * 3)/4
    app.storeAHeight = (app.boardHeight * 2)/4
    app.storeALeft = ((app.spaceWidthPitStore/2 -  app.storeAWidth/2) 
    +app.boardLeft + app.spaceWidthPitStore*7)
    app.storeATop = (app.boardHeight/2 - app.storeAHeight/2) +  app.boardTop
    app.storeAMarbles = []


    app.circlesA = []
    for numPits in range(6):
            cx = (app.boardLeft + app.spaceWidthPitStore * (numPits+1)
            + (app.pitRadius))
            cy = app.boardTop + (app.spaceHeightPit * 2) + app.pitRadius + 55
            app.circlesA.append((cx, cy)) 

    app.marblesA = []
    for cx, cy in app.circlesA:
        app.marblesA.append([(cx, cy), [(cx, cy-7), (cx, cy+7), 
                                 (cx-7, cy), (cx+7, cy)]])
        

    app.circlesB = []
    for numPits in range(6):
            cx = (app.boardLeft + app.spaceWidthPitStore * (numPits+1)
            + (app.pitRadius))
            cy = app.boardTop + app.pitRadius + 17
            app.circlesB.append((cx, cy)) 


    app.marblesB = []
    for cx, cy in app.circlesB:
        app.marblesB.append([(cx, cy), [(cx, cy-7), (cx, cy+7), 
                                 (cx-7, cy), (cx+7, cy)]])

    app.radiusMarble = 3

    app.playerATurn = True 
    app.playerBTurn = False


    app.playerAName = ""
    app.playerBName = ""
    app.messageTurnA = f"{app.playerAName}'s Turn"
    app.messageTurnB = f"{app.playerBName}'s Turn"

    app.gameOver = False 
    app.gameOverMessage = "GAME IS OVER"

    #buttons for mode 
    app.playervsplayerbutton = Button(app.width/2 - 100, 300, 200, 100, "PLAYER VS PLAYER","yellowgreen",pvspmode)
    app.playervsAIbutton = Button(app.width/2 - 100, 450, 200, 100, "PLAYER VS COMPUTER","yellowgreen", pvsAImode)




    #getting the current state of my board
    if app.playerVScomputer!=None and app.playerVScomputer:
        app.state = Board.getBoardState(app)
        app.playerAI = PlayerAI(app, 5 , app.state , True)
    # print("app.statettee", app.state)
    #make an instance for my player that take the depth of minimax, the current state of board and maximizing = True 

################################################################################
#mode choosing screen

def mode_redrawAll(app):
    # drawLabel("Choose the mode you want to play", app.width/2, app.height/2, size = 24)
    app.playervsplayerbutton.draw()
    app.playervsAIbutton.draw()


def mode_onMousePress(app, mouseX, mouseY):
    app.playervsplayerbutton.checkForPress(app, mouseX, mouseY)
    app.playervsAIbutton.checkForPress(app, mouseX, mouseY)

def mode_onMouseMove(app, mouseX, mouseY):
    app.playervsplayerbutton.hoverColor(app, mouseX, mouseY)
    app.playervsAIbutton.hoverColor(app, mouseX, mouseY)
    

def pvspmode(app):
    setActiveScreen('game')
    app.playerVSplayer = True 
    app.playerVScomputer = False

def pvsAImode(app):
    setActiveScreen('game')
    app.playerVSplayer = False
    app.playerVScomputer = True 

#---------------------------------------------------
################################################################################
#enter name screen




#---------------------------------------------------

def game_redrawAll(app):
    for obj in app.objects:
        obj.draw(app)
    app.pitsA.drawMarbles(app)
    app.pitsB.drawMarbles(app)
    app.storeA.drawMarbles(app)
    app.storeB.drawMarbles(app)
    if app.playerATurn and (not app.playerBTurn):
        app.playerA.drawMessageTurnA(app)
    if app.playerBTurn and (not app.playerATurn):
        app.playerB.drawMessageTurnB(app)
    if app.gameOver:
        app.board.drawBoardMessage(app)
        app.board.checkWinner(app)
    # print("app.state", app.state)
        #printing winner, will make it prettier after

# def onMouseMove(app, mouseX, mouseY):
#     pass

def game_onMousePress(app, mouseX, mouseY):
    # app.state = Board.getBoardState(app)
    # app.playerAI = PlayerAI(app, 5 , app.state , True)
    # print("app.state", app.state)
    ##for player vs player mode 
    if app.playerVSplayer:
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
            app.playerB.captureAllRestMarbles(app)
            app.playerA.captureAllRestMarbles(app) 
            app.playerATurn = False 
            app.playerBTurn = False
            return 
    
    #for player vs computer mode 
    elif app.playerVScomputer:
        app.state = Board.getBoardState(app)
        app.playerAI = PlayerAI(app, 5 , app.state , True)
        if not app.gameOver:
            #Human's Turn 
            for cx, cy in app.circlesA:
                if distance(cx, cy, mouseX, mouseY) <= app.pitRadius:
                    if app.playerATurn and (not app.playerBTurn):
                        moveMarblesInPitA(app, cx, cy)
                        

            #opponent's turn 
            for cx, cy in app.circlesB:
                if distance(cx, cy, mouseX, mouseY) <= app.pitRadius:
                    if app.playerBTurn and (not app.playerATurn):
                        moveMarblesInPitBcomputer(app)   
        

        # if pitsA.allEmpty(app)==True or pitsB.allEmpty(app)==True:
        if allEmptyA(app) or allEmptyB(app):
            app.gameOver = True
        
        if app.gameOver:
            app.playerAI.captureAllRestMarbles(app)
            app.playerA.captureAllRestMarbles(app) 
            app.playerATurn = False 
            app.playerBTurn = False
            return 


def moveMarblesInPitA(app, cxTarget, cyTarget):
    indexTarget = PlayerA.getIndexCircleTarget(app, cxTarget, cyTarget)
    if (app.marblesA[indexTarget][1]) != []:
        app.playerA.moveMarblesInpit(app, cxTarget, cyTarget)
    

def moveMarblesInPitB(app, cxTarget, cyTarget):
    indexTarget = PlayerB.getIndexCircleTarget(app, cxTarget, cyTarget)
    if (app.marblesB[indexTarget][1]) != []:
        app.playerB.moveMarblesInpit(app, cxTarget, cyTarget)

def moveMarblesInPitBcomputer(app):
    app.playerAI.moveMarblesInPit(app)

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

# def onStep(app):
#     pass

# runAppWithScreens(initialScreen='mode')

def main():
    runAppWithScreens(initialScreen='mode', width = 800, height = 800)
    runApp(width = 800, height = 800)
    
    

if __name__ == '__main__':
    main() 





##todo
#input names :not in terminal but in screen
#minimax 
# def hoverPit(self): #to change color of pit 
#add the welcome screens and the aurevoir screens
#marble moving animation
#improve UI





#notes 
#deposit marble in my own pit 
    #deposit marble in store 
    #deposit marble in opponent pit
    #if last marble lands in store, take another turn 
    #if last marble lands in my own pit and its empty, 
            # capture that last marble 
            # capture all the marble in opposite pit of the opponent 
