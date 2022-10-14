# CS4750 HW4

from enum import Enum
import copy
import time

class Tile(Enum):
    EMPTY = 0
    X = 1
    O = 2
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
        elif self.board[r-1][c] == Tile.EMPTY and r > 0: #up
            self.board[r-1][c] == Tile.PLAYABLE
        elif self.board[r-1][c+1] == Tile.EMPTY and r > 0 and c <=5: #up and right
            self.board[r-1][c+1] == Tile.PLAYABLE
        elif self.board[r][c-1] == Tile.EMPTY and c > 0: #left
            self.board[r][c-1] == Tile.PLAYABLE
        elif self.board[r][c+1] == Tile.EMPTY and c <= 5: #right
            self.board[r][c+1] == Tile.PLAYABLE
        elif self.board[r+1][c-1] == Tile.EMPTY and r <= 4 and c>0: #down and left
            self.board[r+1][c-1] == Tile.PLAYABLE
        elif self.board[r+1][c] == Tile.EMPTY and r <= 4: #down 
            self.board[r+1][c] == Tile.PLAYABLE
        elif self.board[r+1][c+1] == Tile.EMPTY and r <= 4 and c <=5: #down and right
            self.board[r+1][c+1] == Tile.PLAYABLE

    def getBoard(self):
        return self.board

    def getPlayAt(self, position):
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

    def testMoveForWin(self, position):
        r = position.row
        c = position.col
        friendly_tile = None
        if self.current_players_turn == Player.PLAYER_1:
            friendly_tile = self.p1_tile
        else:
            friendly_tile = self.p2_tile
        #vertical test
        if r - 1 >= 0 and self.board[r-1][c] == friendly_tile:
            pass
        #horizontal test
        #diagonal test


# Returns position for best move to make based on current player
def minimaxDecision(game, maxDepth, totalGenerated):
    # generate list of possible positions to play
    positions_list = game.generatePossiblePlays()
    #total nodes generated during this minimiax decision
    totalGenerated += len(positions_list)
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
    totalGenerated += len(successors)
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
    totalGenerated += len(successors)
    value = None
    for successorGame in successors:
        result = minValue(successorGame, depth + 1, maxDepth, totalGenerated)
        if value is None or value > result:
            value = result
    return value

def evaluator(game_board_state):
    # Initialize evaluation metrics
    two_sequential_two_open_sides_p1 = 0
    two_sequential_one_open_side_p1 = 0
    three_sequential_two_open_sides_p1 = 0
    three_sequential_one_open_side_p1 = 0
    two_sequential_two_open_sides_p2 = 0
    two_sequential_one_open_side_p2 = 0
    three_sequential_two_open_sides_p2 = 0
    three_sequential_one_open_side_p2 = 0

def playTicTacToe(game):
    play = True
    isWinner = False
    while play:
        totalGenerated = 0
        playerOneMove = minimaxDecision(game, Player.PLAYER_1, 2, totalGenerated)
        print("Player 1 placed an X at %d,%d" % (playerOneMove.row+1, playerOneMove.col+1))
        print("Player 1 generated %d nodes during their minimax search" % (totalGenerated))
        isWinner = game.makePlay(playerOneMove)
        print(time.process_time())
        if isWinner:
            play = False
            print("Player 1 has won the game")
        totalGenerated = 0
        playerTwoMove = minimaxDecision(game, Player.PLAYER_2, 4, totalGenerated)
        print("Player 2 has placed an O at %d,%d" % (playerTwoMove.row+1, playerTwoMove.col+1))
        print("Player 2 generated %d nodes during their minimax search" % (totalGenerated))
        isWinner = game.makePlay(playerTwoMove)
        print(time.process_time())
        if isWinner:
            play = False
            print("Player 2 has won the game")


def main():
    game = Game()
    game.makePlay(Player.PLAYER_1, Position(3, 3))
    game.makePlay(Player.PLAYER_2, Position(3, 4))
    game.printBoard()

# Call to main
main()


