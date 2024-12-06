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