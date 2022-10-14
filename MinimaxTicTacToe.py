# CS4750 HW4

from enum import Enum
import copy
import time

class Tile(Enum):
    EMPTY = 0
    X = 1
    O = 2
    INVALID = 4
    PLAYABLE = 3

class Player(Enum):
    PLAYER_1 = 0
    PLAYER_2 = 1

# Groups position together and offsets indexing by 1
class Position:
    def __init__(self, row, col):
        self.row = row - 1
        self.col = col - 1

class Game:
    def __init__(self):
        # Board Dimensions
        self.row_count = 5
        self.col_count = 6

        # A 5 row, 6 column game board whose tiles are empty
        board = []
        for x in range(self.row_count):
            row = []
            for y in range(self.col_count):
                row.append(Tile.EMPTY)
            board.append(row)
        self.board = board

        # Assign Players a tile type
        self.p1_tile = Tile.X
        self.p2_tile = Tile.O

        # Current players turn tracker, always start with one
        self.current_players_turn = Player.PLAYER_1

        # Set to a certain player if they have won
        self.winner = None

    # "Successor function: a player may place a piece at any
    # empty space next to an existing piece horizontally,
    # vertically, or diagonally on the board."
    # Currently assumes valid play is made.
    def generatePossiblePlays(self):
        return [Position(row,col) for row in range(1,self.row_count) for col in range(1,self.col_count) if self.board[row][col] == Tile.PLAYABLE]
    
    def getCurrentPlayersTile(self):
        if self.current_players_turn == Player.PLAYER_1:
            return self.p1_tile
        return self.p2_tile

    def makePlay(self, position):
        r = position.row
        c = position.col
        #set correct tile and alternate which players turn it is
        if self.current_players_turn == Player.PLAYER_1:
            self.board[r][c] = self.p1_tile
            self.current_players_turn = Player.PLAYER_2
        else:
            self.board[r][c] = self.p2_tile
            self.current_players_turn = Player.PLAYER_1

        if self.board[r-1][c-1] == Tile.EMPTY and r>0 and c>0: #up and left
            self.board[r-1][c-1] = Tile.PLAYABLE
        if self.board[r-1][c] == Tile.EMPTY and r > 0: #up
            self.board[r-1][c] = Tile.PLAYABLE
        if self.board[r-1][c+1] == Tile.EMPTY and r > 0 and c <=5: #up and right
            self.board[r-1][c+1] = Tile.PLAYABLE
        if self.board[r][c-1] == Tile.EMPTY and c > 0: #left
            self.board[r][c-1] = Tile.PLAYABLE
        if self.board[r][c+1] == Tile.EMPTY and c <= 5: #right
            self.board[r][c+1] = Tile.PLAYABLE
        if self.board[r+1][c-1] == Tile.EMPTY and r <= 4 and c>0: #down and left
            self.board[r+1][c-1] = Tile.PLAYABLE
        if self.board[r+1][c] == Tile.EMPTY and r <= 4: #down 
            self.board[r+1][c] = Tile.PLAYABLE
        if self.board[r+1][c+1] == Tile.EMPTY and r <= 4 and c <=5: #down and right
            self.board[r+1][c+1] = Tile.PLAYABLE

    def getBoard(self):
        return self.board

    def getPlayAt(self, position):
        if position.row >= 5 or position.row < 0 or position.col >= 6 or position.col < 0:
            return Tile.INVALID
        return self.board[position.row][position.col]

    def tileToString(self, row, col):
        play = self.board[row][col]
        if play == Tile.X:
            return "X"
        elif play == Tile.O:
            return "O"
        else:
            return " "

    # Assumes a fixed width font is used for displaying output
    def printBoard(self):
        print("_________________________")
        for row in range(self.row_count):
            row_string = "| "
            for col in range(self.col_count):
                row_string += self.tileToString(row, col)
                row_string += " | "
            print(row_string)
            print("_________________________")

    def getHeuristic(self):
        twoSideOpen3InARowX = 0
        twoSideOpen3InARowO = 0
        oneSideOpen3InARowX = 0
        oneSideOpen3InARowO = 0
        twoSideOpen2InARowX = 0
        twoSideOpen2InARowO = 0
        oneSideOpen2InARowX = 0
        oneSideOpen2InARowO = 0
        
        toggle = 0
        for row in range(5):
            for col in range(5):
                if (toggle > 0):
                    toggle -= 1
                    continue
                lastTile = self.getPlayAt(Position(row+1, col))
                thisTile = self.getPlayAt(Position(row+1, col+1))
                if thisTile == Tile.O:
                    if self.getPlayAt(Position(row+1, col+2)) == Tile.O:
                        if self.getPlayAt(Position(row+1, col+3)) == Tile.O:
                            if lastTile == Tile.PLAYABLE and self.getPlayAt(Position(row+1, col+4)) == Tile.PLAYABLE:
                                twoSideOpen3InARowO += 1
                            elif lastTile == Tile.PLAYABLE or self.getPlayAt(Position(row+1, col+4)) == Tile.PLAYABLE:
                                oneSideOpen3InARowO += 1
                            toggle += 1
                        elif lastTile == Tile.PLAYABLE and self.getPlayAt(Position(row+1, col+3)) == Tile.PLAYABLE:
                            twoSideOpen2InARowO += 1
                        elif lastTile == Tile.PLAYABLE or self.getPlayAt(Position(row+1, col+3)) == Tile.PLAYABLE:
                            oneSideOpen2InARowO += 1
                elif thisTile == Tile.X:
                    if self.getPlayAt(Position(row+1, col+2)) == Tile.X:
                        if self.getPlayAt(Position(row+1, col+3)) == Tile.X:
                            if lastTile == Tile.PLAYABLE and self.getPlayAt(Position(row+1, col+4)) == Tile.PLAYABLE:
                                twoSideOpen3InARowX += 1
                            elif lastTile == Tile.PLAYABLE or self.getPlayAt(Position(row+1, col+4)) == Tile.PLAYABLE:
                                oneSideOpen3InARowX += 1
                            toggle += 1
                        elif lastTile == Tile.PLAYABLE and self.getPlayAt(Position(row+1, col+3)) == Tile.PLAYABLE:
                            twoSideOpen2InARowX += 1
                        elif lastTile == Tile.PLAYABLE or self.getPlayAt(Position(row+1, col+3)) == Tile.PLAYABLE:
                            oneSideOpen2InARowX += 1
        toggle = 0
        for col in range(6):
            for row in range(4):
                if (toggle > 0):
                    toggle -= 1
                    continue
                lastTile = self.getPlayAt(Position(row, col+1))
                thisTile = self.getPlayAt(Position(row+1, col+1))
                if thisTile == Tile.O:
                    if self.getPlayAt(Position(row+2, col+1)) == Tile.O:
                        if self.getPlayAt(Position(row+3, col+1)) == Tile.O:
                            if lastTile == Tile.PLAYABLE and self.getPlayAt(Position(row+4, col+1)) == Tile.PLAYABLE:
                                twoSideOpen3InARowO += 1
                            elif lastTile == Tile.PLAYABLE or self.getPlayAt(Position(row+4, col+1)) == Tile.PLAYABLE:
                                oneSideOpen3InARowO += 1
                            toggle += 1
                        elif lastTile == Tile.PLAYABLE and self.getPlayAt(Position(row+3, col+1)) == Tile.PLAYABLE:
                            twoSideOpen2InARowO += 1
                        elif lastTile == Tile.PLAYABLE or self.getPlayAt(Position(row+3, col+1)) == Tile.PLAYABLE:
                            oneSideOpen2InARowO += 1
                elif thisTile == Tile.X:
                    if self.getPlayAt(Position(row+2, col+1)) == Tile.X:
                        if self.getPlayAt(Position(row+3, col+1)) == Tile.X:
                            if lastTile == Tile.PLAYABLE and self.getPlayAt(Position(row+4, col+1)) == Tile.PLAYABLE:
                                twoSideOpen3InARowX += 1
                            elif lastTile == Tile.PLAYABLE or self.getPlayAt(Position(row+4, col+1)) == Tile.PLAYABLE:
                                oneSideOpen3InARowX += 1
                            toggle += 1
                        elif lastTile == Tile.PLAYABLE and self.getPlayAt(Position(row+3, col+1)) == Tile.PLAYABLE:
                            twoSideOpen2InARowX += 1
                        elif lastTile == Tile.PLAYABLE or self.getPlayAt(Position(row+3, col+1)) == Tile.PLAYABLE:
                            oneSideOpen2InARowX += 1
        check = []
        row = 0
        while row < 5:
            col = 0
            while col < 5:
                val = (row+1)*10 + (col+1)
                if val in check:
                    check.remove(val)
                    col += 1
                    continue
                lastTile = self.getPlayAt(Position(row, col))
                thisTile = self.getPlayAt(Position(row+1, col+1))
                if thisTile == Tile.O:
                    if self.getPlayAt(Position(row+2, col+2)) == Tile.O:
                        if self.getPlayAt(Position(row+3, col+3)) == Tile.O:
                            if lastTile == Tile.PLAYABLE and self.getPlayAt(Position(row+4, col+4)) == Tile.PLAYABLE:
                                check.append((row+2)*10 + col)
                                twoSideOpen3InARowO += 1
                            elif lastTile == Tile.PLAYABLE or self.getPlayAt(Position(row+4, col+4)) == Tile.PLAYABLE:
                                check.append((row+2)*10 + col)
                                oneSideOpen3InARowO += 1
                        elif lastTile == Tile.PLAYABLE and self.getPlayAt(Position(row+3, col+3)) == Tile.PLAYABLE:
                            twoSideOpen2InARowO += 1
                        elif lastTile == Tile.PLAYABLE or self.getPlayAt(Position(row+3, col+3)) == Tile.PLAYABLE:
                            oneSideOpen2InARowO += 1
                elif thisTile == Tile.X:
                    if self.getPlayAt(Position(row+2, col+2)) == Tile.X:
                        if self.getPlayAt(Position(row+3, col+3)) == Tile.X:
                            if lastTile == Tile.PLAYABLE and self.getPlayAt(Position(row+4, col+4)) == Tile.PLAYABLE:
                                check.append((row+2)*10 + col)
                                twoSideOpen3InARowX += 1
                            elif lastTile == Tile.PLAYABLE or self.getPlayAt(Position(row+4, col+4)) == Tile.PLAYABLE:
                                check.append((row+2)*10 + col)
                                oneSideOpen3InARowX += 1
                        elif lastTile == Tile.PLAYABLE and self.getPlayAt(Position(row+3, col+3)) == Tile.PLAYABLE:
                            twoSideOpen2InARowX += 1
                        elif lastTile == Tile.PLAYABLE or self.getPlayAt(Position(row+3, col+3)) == Tile.PLAYABLE:
                            oneSideOpen2InARowX += 1
                col += 1
            row += 1

        check = []
        row = 0
        while row < 5:
            col = 1
            while col < 6:
                val = (row+1)*10 + (col+1)
                if val in check:
                    check.remove(val)
                    col += 1
                    continue
                lastTile = self.getPlayAt(Position(row, col))
                thisTile = self.getPlayAt(Position(row+1, col+1))
                if thisTile == Tile.O:
                    if self.getPlayAt(Position(row+2, col)) == Tile.O:
                        if self.getPlayAt(Position(row+3, col-1)) == Tile.O:
                            if lastTile == Tile.PLAYABLE and self.getPlayAt(Position(row+4, col-2)) == Tile.PLAYABLE:
                                check.append((row+2)*10 + col)
                                twoSideOpen3InARowO += 1
                            elif lastTile == Tile.PLAYABLE or self.getPlayAt(Position(row+4, col-2)) == Tile.PLAYABLE:
                                check.append((row+2)*10 + col)
                                oneSideOpen3InARowO += 1
                        elif lastTile == Tile.PLAYABLE and self.getPlayAt(Position(row+3, col-1)) == Tile.PLAYABLE:
                            twoSideOpen2InARowO += 1
                        elif lastTile == Tile.PLAYABLE or self.getPlayAt(Position(row+3, col-1)) == Tile.PLAYABLE:
                            oneSideOpen2InARowO += 1
                elif thisTile == Tile.X:
                    if self.getPlayAt(Position(row+2, col)) == Tile.X:
                        if self.getPlayAt(Position(row+3, col-1)) == Tile.X:
                            if lastTile == Tile.PLAYABLE and self.getPlayAt(Position(row+4, col-2)) == Tile.PLAYABLE:
                                check.append((row+2)*10 + col)
                                twoSideOpen3InARowX += 1
                            elif lastTile == Tile.PLAYABLE or self.getPlayAt(Position(row+4, col-2)) == Tile.PLAYABLE:
                                check.append((row+2)*10 + col)
                                oneSideOpen3InARowX += 1
                        elif lastTile == Tile.PLAYABLE and self.getPlayAt(Position(row+3, col-1)) == Tile.PLAYABLE:
                            print(row)
                            print(col)
                            twoSideOpen2InARowX += 1
                        elif lastTile == Tile.PLAYABLE or self.getPlayAt(Position(row+3, col-1)) == Tile.PLAYABLE:
                            oneSideOpen2InARowX += 1
                col += 1
            row += 1
        # print("twoSideOpen3InARowX: " + str(twoSideOpen3InARowX))
        # print("twoSideOpen3InARowO: " + str(twoSideOpen3InARowO))
        # print("oneSideOpen3InARowX: " + str(oneSideOpen3InARowX))
        # print("oneSideOpen3InARowO: " + str(oneSideOpen3InARowO))
        # print("twoSideOpen2InARowX: " + str(twoSideOpen2InARowX))
        # print("twoSideOpen2InARowO: " + str(twoSideOpen2InARowO))
        # print("oneSideOpen2InARowX: " + str(oneSideOpen2InARowX))
        # print("oneSideOpen2InARowO: " + str(oneSideOpen3InARowO))
        if self.getCurrentPlayersTile() == Tile.X:
            return  200*twoSideOpen3InARowX - 80*twoSideOpen3InARowO + 150*oneSideOpen3InARowX - 40*oneSideOpen3InARowO + 20*twoSideOpen2InARowX - 15*twoSideOpen2InARowO + 5*oneSideOpen2InARowX - 2*oneSideOpen2InARowO
        return  200*twoSideOpen3InARowO - 80*twoSideOpen3InARowX + 150*oneSideOpen3InARowO - 40*oneSideOpen3InARowX + 20*twoSideOpen2InARowO - 15*twoSideOpen2InARowX + 5*oneSideOpen2InARowO - 2*oneSideOpen2InARowX


# Returns position for best move to make based on current player
def minimaxDesicion(game_board_state, current_player):
    pass
    # Returns a copy of this game object with the given move applied
    def generateResultOfPlay(self, position):
        result = copy.deepcopy(self)
        result.makePlay(position)
        return result

    # Returns a list of successors to this game object based on all the possible movements
    def generateSuccessors(self):
        positions_list = self.generatePossiblePlays()
        successors = []
        for position in positions_list:
            successors.append(self.generateResultOfPlay(position))

    #Returns true if the move results in a win
    def doesMoveResultInWin(self, position):
        r = position.row
        c = position.col
        friendly_tile = None
        if self.current_players_turn == Player.PLAYER_1:
            friendly_tile = self.p1_tile
        else:
            friendly_tile = self.p2_tile
        # Vertical test - look for 4 sequential in column that was played in
        friendly_tiles_in_row = 0
        for x in range(0, self.row_count - 1):
            if self.board[x][c] == friendly_tile:
                friendly_tiles_in_row += 1
        if friendly_tiles_in_row == 5 or (friendly_tiles_in_row == 4 and \
        (self.board[0][c] != friendly_tile or self.board[self.row_count-1][c] != friendly_tile)):
            return True
        # Horizontal test - look for 4 sequential in the column that was played in
        friendly_tiles_in_col = 0
        if self.board[r][2] == friendly_tile and self.board[r][3] == friendly_tile and \
        (self.board[r][1] == friendly_tile and self.board[r][0] == friendly_tile) or \
        (self.board[r][1] == friendly_tile and self.board[r][4] == friendly_tile) or \
        (self.board[r][4] == friendly_tile and self.board[r][5] == friendly_tile):
            return True
        # Diagonal - STOPPING POINT

        return False


# Returns position for best move to make based on current player
def minimaxDecision(game, maxDepth, totalGenerated):
    # generate list of possible positions to play
    positions_list = game.generatePossiblePlays()
    #total nodes generated during this minimiax decision
    totalGenerated.count += len(positions_list)
    # run min-value function on each resulting game board generated from all possible actions
    best_position = None
    best_position_value = None
    for position in positions_list:
        result = minValue(game.generateResultOfPlay(position), 1, maxDepth, totalGenerated)
        if best_position_value is None or best_position_value > result:
            best_position = position
            best_position_value = result
    # return the action associated with the maximum evaluated value out of the min-value function calls
    return best_position
    # REMEMBER TO CONSIDER TIE BREAKS! "Break ties based on left to right and top to bottom order."

def minValue(game, depth, maxDepth, totalGenerated):
    # cutoff depth
    if depth == maxDepth:
        return evaluator(game)
    # generate successors list
    successors = game.generateSuccessors()
    totalGenerated.count += len(successors)
    value = None
    for successorGame in successors:
        result = maxValue(successorGame, depth + 1, maxDepth, totalGenerated)
        if value is None or value < result:
            value = result
    return value
def maxValue(game, depth, maxDepth, totalGenerated):
    # cutoff depth
    if depth == maxDepth:
        return evaluator(game)
    # generate successors list
    successors = game.generateSuccessors()
    totalGenerated.count += len(successors)
    value = None
    for successorGame in successors:
        result = minValue(successorGame, depth + 1, maxDepth, totalGenerated)
        if value is None or value > result:
            value = result
    return value

def playTicTacToe(game):
    play = True
    isWinner = False
    while play:
        class TotalGenerated:
            def __init__(self):
                count = 0
        totalGenerated = TotalGenerated()
        playerOneMove = minimaxDecision(game, Player.PLAYER_1, 2, totalGenerated)
        print("Player 1 placed an X at %d,%d" % (playerOneMove.row+1, playerOneMove.col+1))
        print("Player 1 generated %d nodes during their minimax search" % (totalGenerated.count))
        isWinner = game.makePlay(playerOneMove)
        print(time.process_time())
        if isWinner:
            play = False
            print("Player 1 has won the game")
        totalGenerated = TotalGenerated()
        playerTwoMove = minimaxDecision(game, Player.PLAYER_2, 4, totalGenerated)
        print("Player 2 has placed an O at %d,%d" % (playerTwoMove.row+1, playerTwoMove.col+1))
        print("Player 2 generated %d nodes during their minimax search" % (totalGenerated.count))
        isWinner = game.makePlay(playerTwoMove)
        print(time.process_time())
        if isWinner:
            play = False
            print("Player 2 has won the game")


def main():
    game = Game()
    game.makePlay(Position(4, 3))
    game.makePlay(Position(3, 3))
    game.makePlay(Position(2, 5))
    game.makePlay(Position(4, 2))
    game.makePlay(Position(3, 4))
    game.printBoard()
    print(game.getHeuristic())

# Call to main
main()


