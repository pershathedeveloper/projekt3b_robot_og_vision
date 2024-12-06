#!/usr/bin/env python3
########################################################################
# Filename    : Keypad.py
# Description : The module of matrix keypad 
# Author      : freenove
# modification: 2016/07/13
########################################################################
import RPi.GPIO as GPIO 
import time
#class Key:Define some of the properties of Key
class Key(object):
    NO_KEY = '\0'
    #Defines the four states of Key
    IDLE = 0
    PRESSED = 1
    HOLD = 2
    RELEASED = 3
    #define OPEN and CLOSED
    OPEN = 0
    CLOSED =1
    #constructor
    def __init__(self):
        self.kchar = self.NO_KEY
        self.kstate = self.IDLE
        self.kcode = -1
        self.stateChanged = False

class Keypad(object):
    NULL = '\0'
    LIST_MAX = 10   #Max number of keys on the active list.
    MAPSIZE = 10    #MAPSIZE is the number of rows (times 16 columns)
    bitMap = [0]*MAPSIZE
    key = [Key()]*LIST_MAX
    holdTime = 500      #key hold time
    holdTimer = 0
    startTime = 0
    #Allows custom keymap, pin configuration, and keypad sizes.
    def __init__(self,usrKeyMap,row_Pins,col_Pins,num_Rows,num_Cols):
        GPIO.setmode(GPIO.BOARD)
        self.rowPins = row_Pins
        self.colPins = col_Pins
        self.numRows = num_Rows
        self.numCols = num_Cols
        
        self.keymap = usrKeyMap
        self.setDebounceTime(10)
    #Returns a single key only. Retained for backwards compatibility.   
    def getKey(self):
        single_key = True
        if(self.getKeys() and self.key[0].stateChanged and (self.key[0].kstate == self.key[0].PRESSED)):
            return self.key[0].kchar
        single_key = False
        return self.key[0].NO_KEY
    #Populate the key list. 
    def getKeys(self):
        keyActivity = False
        #Limit how often the keypad is scanned.
        if((time.time() - self.startTime) > self.debounceTime*0.001):
            self.scanKeys()
            keyActivity = self.updateList()
            self.startTime = time.time()
        return keyActivity
    #Hardware scan ,the result store in bitMap  
    def scanKeys(self):
        #Re-intialize the row pins. Allows sharing these pins with other hardware.
        for pin_r in self.rowPins:
            GPIO.setup(pin_r,GPIO.IN,pull_up_down = GPIO.PUD_UP)
        #bitMap stores ALL the keys that are being pressed.
        for pin_c in self.colPins:
            GPIO.setup(pin_c,GPIO.OUT)
            GPIO.output(pin_c,GPIO.LOW)
            for r in self.rowPins: #keypress is active low so invert to high.
                self.bitMap[self.rowPins.index(r)] = self.bitWrite(self.bitMap[self.rowPins.index(r)],self.colPins.index(pin_c),not GPIO.input(r))
            #Set pin to high impedance input. Effectively ends column pulse.
            GPIO.output(pin_c,GPIO.HIGH)
            GPIO.setup(pin_c,GPIO.IN)
    #Manage the list without rearranging the keys. Returns true if any keys on the list changed state.      
    def updateList(self):
        anyActivity = False
        kk = Key()
        #Delete any IDLE keys
        for i in range(self.LIST_MAX):
            if(self.key[i].kstate == kk.IDLE):
                self.key[i].kchar = kk.NO_KEY
                self.key[i].kcode = -1
                self.key[i].stateChanged = False
        # Add new keys to empty slots in the key list.
        for r in range(self.numRows):
            for c in range(self.numCols):
                button = self.bitRead(self.bitMap[r],c)
                keyChar = self.keymap[r * self.numCols +c]
                keyCode = r * self.numCols +c
                idx = self.findInList(keyCode)
                #Key is already on the list so set its next state.
                if(idx > -1):
                    self.nextKeyState(idx,button)
                #Key is NOT on the list so add it.
                if((idx == -1) and button):
                    for i in range(self.LIST_MAX):
                        if(self.key[i].kchar == kk.NO_KEY): #Find an empty slot or don't add key to list.
                            self.key[i].kchar = keyChar
                            self.key[i].kcode = keyCode
                            self.key[i].kstate = kk.IDLE    #Keys NOT on the list have an initial state of IDLE.
                            self.nextKeyState(i,button)
                            break   #Don't fill all the empty slots with the same key.
        #Report if the user changed the state of any key.
        for i in range(self.LIST_MAX):
            if(self.key[i].stateChanged):
                anyActivity = True
        return anyActivity      
    #This function is a state machine but is also used for debouncing the keys. 
    def nextKeyState(self,idx, button):
        self.key[idx].stateChanged = False
        kk = Key()
        if(self.key[idx].kstate == kk.IDLE):
            if(button == kk.CLOSED):
                self.transitionTo(idx,kk.PRESSED)
                self.holdTimer = time.time()    #Get ready for next HOLD state.
        elif(self.key[idx].kstate == kk.PRESSED):
            if((time.time() - self.holdTimer) > self.holdTime*0.001):   #Waiting for a key HOLD...  
                self.transitionTo(idx,kk.HOLD)
            elif(button == kk.OPEN):        # or for a key to be RELEASED.
                self.transitionTo(idx,kk.RELEASED)
        elif(self.key[idx].kstate == kk.HOLD):
            if(button == kk.OPEN):
                self.transitionTo(idx,kk.RELEASED)
        elif(self.key[idx].kstate == kk.RELEASED):
            self.transitionTo(idx,kk.IDLE)
            
    def transitionTo(self,idx,nextState):
        self.key[idx].kstate = nextState
        self.key[idx].stateChanged = True
    #Search by code for a key in the list of active keys.
    #Returns -1 if not found or the index into the list of active keys.
    def findInList(self,keyCode):
        for i in range(self.LIST_MAX):
            if(self.key[i].kcode == keyCode):
                return i
        return -1
    #set Debounce Time, The default is 50ms                 
    def setDebounceTime(self,ms):
        self.debounceTime = ms
    #set HoldTime,The default is 500ms
    def setHoldTime(self,ms):
        self.holdTime = ms
    #   
    def isPressed(keyChar):
        for i in range(self.LIST_MAX):
            if(self.key[i].kchar == keyChar):
                if(self.key[i].kstate == self.self.key[i].PRESSED and self.key[i].stateChanged):
                    return True
        return False
    #           
    def waitForKey():
        kk = Key()
        waitKey = kk.NO_KEY
        while(waitKey == kk.NO_KEY):
            waitKey = getKey()
        return waitKey
    
    def getState():
        return self.key[0].kstate
    #   
    def keyStateChanged():
        return self.key[0].stateChanged
    
    def bitWrite(self,x,n,b):
        if(b):
            x |= (1<<n)
        else:
            x &=(~(1<<n))
        return x
    def bitRead(self,x,n):
        if((x>>n)&1 == 1):
            return True
        else:
            return False

#######################EXAMPLE##################################        
ROWS = 4
COLS = 4
keys =  [   '1','2','3','A',
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D'     ]
rowsPins = [12,16,18,22]
colsPins = [19,15,13,11]    

def loop():
    keypad = Keypad(keys,rowsPins,colsPins,ROWS,COLS)
    keypad.setDebounceTime(50)
    while(True):
        key = keypad.getKey()
        if(key != keypad.NULL):
            print ("You Pressed Key : %c "%(key) )
            
if __name__ == '__main__':     # Program start from here
    print ("Program is starting ... ")
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        pass
        GPIO.cleanup()  
            
from states import TTTmachine, Init

machine = TTTmachine(Init())
machine.Run()

#!/usr/bin/env python3
########################################################################
# Filename    : MatrixKeypad.py
# Description : obtain the key code of 4x4 Matrix Keypad
# Author      : freenove
# modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
import Keypad       #import module Keypad
ROWS = 4        # number of rows of the Keypad
COLS = 4        #number of columns of the Keypad
keys =  [   '1','2','3','A',    #key code
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D'     ]
rowsPins = [12,16,18,22]        #connect to the row pinouts of the keypad
colsPins = [19,15,13,11]        #connect to the column pinouts of the keypad

def loop():
    keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)    #creat Keypad object
    keypad.setDebounceTime(50)      #set the debounce time
    while(True):
        key = keypad.getKey()       #obtain the state of keys
        if(key != keypad.NULL):     #if there is key pressed, print its key code.
            print ("You Pressed Key : %c "%(key))
            
if __name__ == '__main__':     #Program start from here
    print ("Program is starting ... ")
    try:
        loop()
    except KeyboardInterrupt:  #When 'Ctrl+C' is pressed, exit the program. 
        GPIO.cleanup()

# Implementation of a state machine for running states
class State:
    pass

class StateMachine:
    def __init__(self, state: State):
        self.state: State = state
        self.state.stateMachine = self

    def Run(self):
        self.state.Enter()
        self.running = True
        while self.running:
            self.state.Execute()

    def ChangeState(self, newState: State):
        self.state.Exit()
        self.state = newState
        self.state.stateMachine = self
        self.state.Enter()

# Super class for a state object
class State:
    stateMachine : StateMachine = None

    def Execute(self):
        pass

    def Enter(self):
        pass

    def Exit(self):
        pass

from statemachine import *
from TicTacToeSolver import TicTacToeManager
import socket

class TTTmachine(StateMachine):
    def __init__(self, state: State):
        super().__init__(state)
        self.tttManager = TicTacToeManager()
        self.tttManager.printBoard()
        self.playerToken = "x"
        self.aiToken = "o"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.robotSock = None
        self.useCMDInput = False
        if not self.useCMDInput:
            import RPi.GPIO as GPIO
            import Keypad
            ROWS = 4
            COLS = 4
            keys =  ['1','2','3','A',
                     '4','5','6','B',
                     '7','8','9','C',
                     '*','0','#','D']
            rowsPins = [12,16,18,22]
            colsPins = [19,15,13,11]
            self.keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)
            self.keypad.setDebounceTime(50)

class Init(State):
    def Enter(self):
        self.stateMachine.sock.bind(('192.168.1.42', 9090))
        print("Listening for robot...")
        self.stateMachine.sock.listen(1)
        self.stateMachine.robotSock, addr = self.stateMachine.sock.accept()
        print("Robot connected:", addr)
        self.stateMachine.ChangeState(Idle())
        return

class Idle(State):
    def Execute(self):
        userIn = ""
        if self.stateMachine.useCMDInput:
            userIn = input("Idle: ")
        else:
            userIn = self.keypadInput()

        if userIn == "A":
            self.stateMachine.ChangeState(NewGameSetup())
            return
        elif userIn == "D":
            self.stateMachine.running = False
            return
    
    def keypadInput(self):
        key = self.stateMachine.keypad.getKey()
        if(key != self.stateMachine.keypad.NULL):
            return key
        else:
            return "-1"

class NewGameSetup(State):
    def Enter(self):
        if self.stateMachine.tttManager.isEmpty():
            self.stateMachine.ChangeState(PlayerInput())
            return
        else:
            for i in range(3):
                for j in range(3):
                    if not self.stateMachine.tttManager.isMoveValid(i, j):
                        if self.stateMachine.tttManager.currentBoard.slots[i, j] == self.stateMachine.playerToken:
                            dataSend = ("(" + str(i) + "," + str(j) + ",2)").encode()
                        else:
                            dataSend = ("(" + str(i) + "," + str(j) + ",3)").encode()
                        self.stateMachine.robotSock.sendall(dataSend)
                        while True:
                            dataRecv = self.stateMachine.robotSock.recv(4096)
                            print(dataRecv)
                            if dataRecv == b"Done":
                                break
            self.stateMachine.tttManager.setBoardEmpty()
            self.stateMachine.ChangeState(PlayerInput())
            return

class PlayerInput(State):
    def Execute(self):
        input = "-1"
        if self.stateMachine.useCMDInput:
            input = self.CMDInput()
        else:
            input = self.keypadInput()

        #print("input: ", input)
        
        if input == "-1":
            return
        
        try:
            input = int(input)
        except:
            return

        if (input > 0) and (input < 10):
            if self.stateMachine.tttManager.isMoveValid(int((input - 1)/3), (input - 1)%3):
                self.stateMachine.tttManager.addMove(int((input - 1)/3), (input - 1)%3, self.stateMachine.playerToken)
                self.stateMachine.tttManager.printBoard()
                self.stateMachine.ChangeState(RobotMovePlayer([int((input - 1)/3), (input - 1)%3]))
                return

    def keypadInput(self):
        key = self.stateMachine.keypad.getKey()
        if(key != self.stateMachine.keypad.NULL):
            return key
        else:
            return "-1"

    def CMDInput(self):
        userIn = input("Player move: ")
        return userIn

class RobotMovePlayer(State):
    def __init__(self, move) -> None:
        self.move = move

    def Enter(self):
        # Start moving robot
        dataSend = ("(" + str(self.move[0]) + "," + str(self.move[1]) + ",1)").encode()
        self.stateMachine.robotSock.sendall(dataSend)
        while True:
            dataRecv = self.stateMachine.robotSock.recv(4096)
            print(dataRecv)
            if dataRecv == b"Done":
                break

        # Check if win/draw
        if self.stateMachine.tttManager.isWon(self.stateMachine.playerToken):
            print("PLAYER WIN")
            self.stateMachine.ChangeState(Idle())
            return
        if self.stateMachine.tttManager.isFull():
            print("DRAW")
            self.stateMachine.ChangeState(Idle())
            return
        else:
            self.stateMachine.ChangeState(AICalcMove())
            return

class AICalcMove(State):
    def Enter(self):
        bestMove = self.stateMachine.tttManager.getNewMove(self.stateMachine.aiToken, self.stateMachine.playerToken, 5)
        self.stateMachine.tttManager.addMove(bestMove[0], bestMove[1], self.stateMachine.aiToken)
        self.stateMachine.tttManager.printBoard()
        self.stateMachine.ChangeState(RobotMoveAI(bestMove))

class RobotMoveAI(State):
    def __init__(self, move) -> None:
        self.move = move

    def Enter(self):
        # Start moving robot
        dataSend = ("(" + str(self.move[0]) + "," + str(self.move[1]) + ",0)").encode()
        self.stateMachine.robotSock.sendall(dataSend)
        while True:
            dataRecv = self.stateMachine.robotSock.recv(4096)
            print(dataRecv)
            if dataRecv == b"Done":
                break

        #Check for win/draw
        if self.stateMachine.tttManager.isWon(self.stateMachine.aiToken):
            print("AI WIN")
            self.stateMachine.ChangeState(Idle())
            return
        if self.stateMachine.tttManager.isFull():
            print("DRAW")
            self.stateMachine.ChangeState(Idle())
            return
        else:
            self.stateMachine.ChangeState(PlayerInput())
            return
            

import numpy as np

class Board:
    def __init__(self, slots = np.array([["","",""], ["","",""], ["","",""]])) -> None:
        self.slots = slots

    def setBoard(self, slots) -> None:
        self.slots = slots

    def printBoard(self) -> None:
        print(self.slots[0])
        print(self.slots[1])
        print(self.slots[2])
        print("\n")

    def changeSlot(self, x:int, y:int, newValue) -> None:
        self.slots[x, y] = newValue

    def isEmpty(self, keywordEmpty) -> bool:
        #print(self.slots, keywordEmpty, np.all(self.slots == keywordEmpty))
        return np.all(self.slots == keywordEmpty)

    def isWon(self, key1, key2) -> str: # return "white" or "black" or "false"
        if self.checkWin(key1):
            return key1
        elif self.checkWin(key2):
            return key2
        return "false"

    def checkWin(self, keyword) -> bool:
        if self.checkHorizontal(keyword):
            return True
        elif self.checkVertical(keyword):
            return True
        elif self.checkCross(keyword):
            return True
        return False

    def checkHorizontal(self, keyword) -> bool:
        for i in self.slots:
            if (i == np.array([keyword, keyword, keyword])).all():
                #print("won h")
                return True
        return False

    def checkVertical(self, keyword) -> bool:
        for i in range(3):
            if (self.slots[0, i] == keyword) and (self.slots[1, i] == keyword) and (self.slots[2, i] == keyword):
                #print("won v")
                return True
        return False

    def checkCross(self, keyword) -> bool:
        if self.slots[1,1] == keyword:
            if (self.slots[0,2] == keyword) and (self.slots[2,0] == keyword):
                #print("won c")
                return True
            elif (self.slots[0,0] == keyword) and (self.slots[2,2] == keyword):
                #print("won c")
                return True
        return False

class TicTacToeManager:
    def __init__(self, keywordEmpty:str = "e", boardInit = "auto") -> None:
        self.keywordEmpty = keywordEmpty
        if type(boardInit) == str:
            if boardInit == "auto":
                self.currentBoard = Board(np.array([[keywordEmpty,keywordEmpty,keywordEmpty],
                                                    [keywordEmpty,keywordEmpty,keywordEmpty],
                                                    [keywordEmpty,keywordEmpty,keywordEmpty]]))
        else:
            self.currentBoard = Board(boardInit)

    def setBoardValues(self, newValues = np.array([["","",""], ["","",""], ["","",""]])) -> None:
        self.currentBoard.setBoard(newValues)
    
    def setBoardEmpty(self):
        self.currentBoard = Board(np.array([[self.keywordEmpty,self.keywordEmpty,self.keywordEmpty],
                                            [self.keywordEmpty,self.keywordEmpty,self.keywordEmpty],
                                            [self.keywordEmpty,self.keywordEmpty,self.keywordEmpty]]))

    def printBoard(self):
        self.currentBoard.printBoard()

    def isEmpty(self):
        return self.currentBoard.isEmpty(self.keywordEmpty)
    
    def isMoveValid(self, x, y):
        return self.currentBoard.slots[x, y] == self.keywordEmpty

    def addMove(self, x:int, y:int, newValue) -> None:
        self.currentBoard.changeSlot(x, y, newValue)

    def isWon(self, keyword) -> bool:
        return self.currentBoard.checkWin(keyword)
    
    def isFull(self) -> bool:
        count = np.count_nonzero(self.currentBoard.slots == self.keywordEmpty)
        if count <= 1:
            return True
        return False

    def getNewMove(self, keywordSelf, keywordCompetitor, depth) -> list: # [x, y] on the move
        possibleMoves = self.getPossibleMoves(self.currentBoard)
        if not possibleMoves:
            return [-1, -1]

        scoredMoves = []
        for move in possibleMoves:
            #print("Move:", move)
            score = self.scoreMove(self.currentBoard, move, keywordSelf, keywordCompetitor, True, depth, depth)
            #print("Score:", score)
            #print("\n")
            scoredMoves.append([move, score])
        bestMove = scoredMoves[0]
        for scoredMove in scoredMoves:
            if scoredMove[1] > bestMove[1]:
                bestMove = scoredMove
        return bestMove[0]


    def getPossibleMoves(self, board) -> list:
        possibleMoves = []
        for i in range(3):
            for j in range(3):
                if board.slots[i, j] == self.keywordEmpty:
                    possibleMoves.append([i, j])
        #print(possibleMoves)
        return possibleMoves

    def scoreMove(self, board:Board, move, keywordSelf, KeywordCompetitor, maximize:bool, depth, maxDepth):
        boardCopy:Board = Board(np.copy(board.slots))
        if maximize:
            boardCopy.changeSlot(move[0], move[1], keywordSelf)
            if boardCopy.checkWin(keywordSelf):
                #print("win", depth)
                #print(boardCopy.slots[0])
                #print(boardCopy.slots[1])
                #print(boardCopy.slots[2])
                return 1 + depth
        else:
            boardCopy.changeSlot(move[0], move[1], KeywordCompetitor)
            if boardCopy.checkWin(KeywordCompetitor):
                #print("lose")
                #print(boardCopy.slots[0])
                #print(boardCopy.slots[1])
                #print(boardCopy.slots[2])
                return -1
        #print(boardCopy.slots[0])
        #print(boardCopy.slots[1])
        #print(boardCopy.slots[2])
        #print("\n")
        if depth <= 0:
            #print("depth reach")
            return 0


        possibleMoves = self.getPossibleMoves(boardCopy)
        if not possibleMoves:
            #print("no moves")
            return 0

        scores = []
        for newMove in possibleMoves:
            newMoveScore = self.scoreMove(boardCopy, newMove, keywordSelf, KeywordCompetitor, not maximize, depth - 1, maxDepth)
            #print("NewMove", depth - 1, not maximize, newMove, newMoveScore)
            scores.append(newMoveScore)
        
        #print(maximize, scores)
        if not maximize:
            #print(max(scores))
            return max(scores)
        else:
            #print(min(scores))
            return min(scores)



# Test
if __name__ == "__main__":
    import random
    values = ["w", "b", "e"]
    randomBoardInit = np.array([[values[random.randint(0,2)], values[random.randint(0,2)], values[random.randint(0,2)]],
                           [values[random.randint(0,2)], values[random.randint(0,2)], values[random.randint(0,2)]],
                           [values[random.randint(0,2)], values[random.randint(0,2)], values[random.randint(0,2)]]])
    test = Board(randomBoardInit)
    #print(test.slots[0])
    #print(test.slots[1])
    #print(test.slots[2])
    #print("Result:", test.isWon("w", "b"))
    #print("\n")


    test2 = np.array([['w','e','b'],
                      ['b','w','b'],
                      ['w','e','e']])

    test3 = np.array([['e','b','e'],
                      ['w','b','e'],
                      ['b','e','w']])

    test4 = np.array([['b','e','w'],
                      ['e','w','e'],
                      ['b','e','e']])

    test5 = np.array([['b','e','w'],
                      ['e','e','e'],
                      ['b','e','w']])

    test6 = np.array([['e','e','w'],
                      ['b','e','e'],
                      ['b','e','w']])

    tttManager = TicTacToeManager(boardInit=test6)
    print(tttManager.currentBoard.slots[0])
    print(tttManager.currentBoard.slots[1])
    print(tttManager.currentBoard.slots[2])
    print("\n")
    print(tttManager.getNewMove("w", "b", 4))