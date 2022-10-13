# CS4750 HW4

from enum import Enum
import copy

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

    # "Successor function: a player may place a piece at any
    # empty space next to an existing piece horizontally,
    # vertically, or diagonally on the board."
    # Currently assumes valid play is made.
    def generatePossiblePlays(self):
        return [Position(row,col) for row in range(1,self.row_count) for col in range(1,self.col_count) if self.board[row][col] == Tile.PLAYABLE]

    def makePlay(self, player, position):
        r = position.row
        c = position.col
        if player == Player.PLAYER_1:
            self.board[r][c] = self.p1_tile
        else:
            self.board[r][c] = self.p2_tile

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
    def generateResultOfPlay(self, player, position):
        result = copy.deepcopy(self)
        result.makePlay(player, position)
        return result

    # Returns a list of successors to this game object based on all the possible movements
    def generateSuccessors(self, player):
        positions_list = self.generatePossiblePlays()
        successors = []
        for position in positions_list:
            successors.append(self.generateResultOfPlay(player, position))

# Returns position for best move to make based on current player
def minimaxDecision(game, player, maxDepth):
    # generate list of possible positions to play
    positions_list = game.generatePossiblePlays()
    # run min-value function on each resulting game board generated from all possible actions
    best_position = None
    best_position_value = None
    for position in positions_list:
        result = minValue(game.generateResultOfPlay(player, position), player, 1, maxDepth)
        if best_position_value is None or best_position_value > result:
            best_position = position
            best_position_value = result
    # return the action associated with the maximum evaluated value out of the min-value function calls
    return best_position
    # REMEMBER TO CONSIDER TIE BREAKS! "Break ties based on left to right and top to bottom order."

def minValue(game, player, depth, maxDepth):
    # cutoff depth
    if depth == maxDepth:
        return evaluator(game, player)
    # generate successors list
    successors = game.generateSuccessors(player)
    value = None
    for successorGame in successors:
        result = maxValue(successorGame, player, depth + 1, maxDepth)
        if value is None or value < result:
            value = result
    return value
def maxValue(game, player, depth, maxDepth):
    # cutoff depth
    if depth == maxDepth:
        return evaluator(game, player)
    # generate successors list
    successors = game.generateSuccessors(player)
    value = None
    for successorGame in successors:
        result = minValue(successorGame, player, depth + 1, maxDepth)
        if value is None or value > result:
            value = result
    return value

def evaluator(game_board_state, current_player):
    # Initialize evaluation metrics
    two_sequential_two_open_sides_p1 = 0
    two_sequential_one_open_side_p1 = 0
    three_sequential_two_open_sides_p1 = 0
    three_sequential_one_open_side_p1 = 0
    two_sequential_two_open_sides_p2 = 0
    two_sequential_one_open_side_p2 = 0
    three_sequential_two_open_sides_p2 = 0
    three_sequential_one_open_side_p2 = 0

def main():
    game = Game()
    game.makePlay(Player.PLAYER_1, Position(3, 3))
    game.makePlay(Player.PLAYER_2, Position(3, 4))
    game.printBoard()

# Call to main
main()


