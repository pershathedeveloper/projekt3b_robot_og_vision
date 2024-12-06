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