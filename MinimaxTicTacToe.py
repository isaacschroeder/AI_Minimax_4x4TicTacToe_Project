# CS4750 HW4

from enum import Enum


class Tile(Enum):
    EMPTY = 0
    X = 1
    O = 2
    INVALID = 4

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
    def makePlay(self, player, position):
        if player == Player.PLAYER_1:
            self.board[position.row][position.col] = self.p1_tile
        else:
            self.board[position.row][position.col] = self.p2_tile

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

    def getH(self):
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
                            if lastTile == Tile.EMPTY and self.getPlayAt(Position(row+1, col+4)) == Tile.EMPTY:
                                twoSideOpen3InARowO += 1
                            elif lastTile == Tile.EMPTY or self.getPlayAt(Position(row+1, col+4)) == Tile.EMPTY:
                                oneSideOpen3InARowO += 1
                            toggle += 1
                        elif lastTile == Tile.EMPTY and self.getPlayAt(Position(row+1, col+3)) == Tile.EMPTY:
                            twoSideOpen2InARowO += 1
                        elif lastTile == Tile.EMPTY or self.getPlayAt(Position(row+1, col+3)) == Tile.EMPTY:
                            oneSideOpen2InARowO += 1
                elif thisTile == Tile.X:
                    if self.getPlayAt(Position(row+1, col+2)) == Tile.X:
                        if self.getPlayAt(Position(row+1, col+3)) == Tile.X:
                            if lastTile == Tile.EMPTY and self.getPlayAt(Position(row+1, col+4)) == Tile.EMPTY:
                                twoSideOpen3InARowX += 1
                            elif lastTile == Tile.EMPTY or self.getPlayAt(Position(row+1, col+4)) == Tile.EMPTY:
                                oneSideOpen3InARowX += 1
                            toggle += 1
                        elif lastTile == Tile.EMPTY and self.getPlayAt(Position(row+1, col+3)) == Tile.EMPTY:
                            twoSideOpen2InARowX += 1
                        elif lastTile == Tile.EMPTY or self.getPlayAt(Position(row+1, col+3)) == Tile.EMPTY:
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
                            if lastTile == Tile.EMPTY and self.getPlayAt(Position(row+4, col+1)) == Tile.EMPTY:
                                twoSideOpen3InARowO += 1
                            elif lastTile == Tile.EMPTY or self.getPlayAt(Position(row+4, col+1)) == Tile.EMPTY:
                                oneSideOpen3InARowO += 1
                            toggle += 1
                        elif lastTile == Tile.EMPTY and self.getPlayAt(Position(row+3, col+1)) == Tile.EMPTY:
                            twoSideOpen2InARowO += 1
                        elif lastTile == Tile.EMPTY or self.getPlayAt(Position(row+3, col+1)) == Tile.EMPTY:
                            oneSideOpen2InARowO += 1
                elif thisTile == Tile.X:
                    if self.getPlayAt(Position(row+2, col+1)) == Tile.X:
                        if self.getPlayAt(Position(row+3, col+1)) == Tile.X:
                            if lastTile == Tile.EMPTY and self.getPlayAt(Position(row+4, col+1)) == Tile.EMPTY:
                                twoSideOpen3InARowX += 1
                            elif lastTile == Tile.EMPTY or self.getPlayAt(Position(row+4, col+1)) == Tile.EMPTY:
                                oneSideOpen3InARowX += 1
                            toggle += 1
                        elif lastTile == Tile.EMPTY and self.getPlayAt(Position(row+3, col+1)) == Tile.EMPTY:
                            twoSideOpen2InARowX += 1
                        elif lastTile == Tile.EMPTY or self.getPlayAt(Position(row+3, col+1)) == Tile.EMPTY:
                            oneSideOpen2InARowX += 1
        check = []
        row = 0
        while row < 5:
            col = 0
            while col < 5:
                val = row*10 + col
                if val in check:
                    check.remove(val)
                    col += 1
                    continue
                lastTile = self.getPlayAt(Position(row, col))
                thisTile = self.getPlayAt(Position(row+1, col+1))
                if thisTile == Tile.O:
                    if self.getPlayAt(Position(row+2, col+2)) == Tile.O:
                        if self.getPlayAt(Position(row+3, col+3)) == Tile.O:
                            if lastTile == Tile.EMPTY and self.getPlayAt(Position(row+4, col+4)) == Tile.EMPTY:
                                check.append((row+2)*10 + col)
                                check.append((row+3)*10 + col - 1)
                                twoSideOpen3InARowO += 1
                            elif lastTile == Tile.EMPTY or self.getPlayAt(Position(row+4, col+4)) == Tile.EMPTY:
                                check.append((row+2)*10 + col)
                                check.append((row+3)*10 + col - 1)
                                oneSideOpen3InARowO += 1
                        elif lastTile == Tile.EMPTY and self.getPlayAt(Position(row+3, col+3)) == Tile.EMPTY:
                            twoSideOpen2InARowO += 1
                        elif lastTile == Tile.EMPTY or self.getPlayAt(Position(row+3, col+3)) == Tile.EMPTY:
                            oneSideOpen2InARowO += 1
                elif thisTile == Tile.X:
                    if self.getPlayAt(Position(row+2, col+2)) == Tile.X:
                        if self.getPlayAt(Position(row+3, col+3)) == Tile.X:
                            if lastTile == Tile.EMPTY and self.getPlayAt(Position(row+4, col+4)) == Tile.EMPTY:
                                check.append((row+2)*10 + col)
                                check.append((row+3)*10 + col - 1)
                                twoSideOpen3InARowX += 1
                            elif lastTile == Tile.EMPTY or self.getPlayAt(Position(row+4, col+4)) == Tile.EMPTY:
                                check.append((row+2)*10 + col)
                                check.append((row+3)*10 + col - 1)
                                oneSideOpen3InARowX += 1
                        elif lastTile == Tile.EMPTY and self.getPlayAt(Position(row+3, col+3)) == Tile.EMPTY:
                            twoSideOpen2InARowX += 1
                        elif lastTile == Tile.EMPTY or self.getPlayAt(Position(row+3, col+3)) == Tile.EMPTY:
                            oneSideOpen2InARowX += 1
                col += 1
            row += 1

        check = []
        row = 0
        while row < 5:
            col = 2
            while col < 6:
                print(col)
                val = row*10 + col
                if val in check:
                    print(val)
                    print(check)
                    check.remove(val)
                    col += 1
                    continue
                lastTile = self.getPlayAt(Position(row, col))
                thisTile = self.getPlayAt(Position(row+1, col+1))
                if thisTile == Tile.O:
                    if self.getPlayAt(Position(row+2, col)) == Tile.O:
                        if self.getPlayAt(Position(row+3, col-1)) == Tile.O:
                            if lastTile == Tile.EMPTY and self.getPlayAt(Position(row+4, col-2)) == Tile.EMPTY:
                                check.append((row+2)*10 + col)
                                check.append((row+3)*10 + col - 1)
                                twoSideOpen3InARowO += 1
                            elif lastTile == Tile.EMPTY or self.getPlayAt(Position(row+4, col-2)) == Tile.EMPTY:
                                check.append((row+2)*10 + col)
                                check.append((row+3)*10 + col - 1)
                                oneSideOpen3InARowO += 1
                        elif lastTile == Tile.EMPTY and self.getPlayAt(Position(row+3, col-1)) == Tile.EMPTY:
                            twoSideOpen2InARowO += 1
                        elif lastTile == Tile.EMPTY or self.getPlayAt(Position(row+3, col-1)) == Tile.EMPTY:
                            oneSideOpen2InARowO += 1
                elif thisTile == Tile.X:
                    if self.getPlayAt(Position(row+2, col)) == Tile.X:
                        if self.getPlayAt(Position(row+3, col-1)) == Tile.X:
                            if lastTile == Tile.EMPTY and self.getPlayAt(Position(row+4, col-2)) == Tile.EMPTY:
                                check.append((row+2)*10 + col)
                                check.append((row+3)*10 + col - 1)
                                twoSideOpen3InARowX += 1
                            elif lastTile == Tile.EMPTY or self.getPlayAt(Position(row+4, col-2)) == Tile.EMPTY:
                                check.append((row+2)*10 + col)
                                check.append((row+3)*10 + col - 1)
                                oneSideOpen3InARowX += 1
                        elif lastTile == Tile.EMPTY and self.getPlayAt(Position(row+3, col-1)) == Tile.EMPTY:
                            print(row)
                            print(col)
                            twoSideOpen2InARowX += 1
                        elif lastTile == Tile.EMPTY or self.getPlayAt(Position(row+3, col-1)) == Tile.EMPTY:
                            oneSideOpen2InARowX += 1
                col += 1
            row += 1
        print("twoSideOpen3InARowX: " + str(twoSideOpen3InARowX))
        print("twoSideOpen3InARowO: " + str(twoSideOpen3InARowO))
        print("oneSideOpen3InARowX: " + str(oneSideOpen3InARowX))
        print("oneSideOpen3InARowO: " + str(oneSideOpen3InARowO))
        print("twoSideOpen2InARowX: " + str(twoSideOpen2InARowX))
        print("twoSideOpen2InARowO: " + str(twoSideOpen2InARowO))
        print("oneSideOpen2InARowX: " + str(oneSideOpen2InARowX))
        print("oneSideOpen2InARowO: " + str(oneSideOpen3InARowO))
        return  200*twoSideOpen3InARowX - 80*twoSideOpen3InARowO + 150*oneSideOpen3InARowX - 40*oneSideOpen3InARowO + 20*twoSideOpen2InARowX - 15*twoSideOpen2InARowO + 5*oneSideOpen2InARowX - 2*oneSideOpen2InARowO


# Returns position for best move to make based on current player
def minimaxDesicion(game_board_state, current_player):
    pass

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
    # game.makePlay(Player.PLAYER_1, Position(4, 1))
    # game.makePlay(Player.PLAYER_1, Position(3, 2))
    # game.makePlay(Player.PLAYER_1, Position(2, 3))
    # game.makePlay(Player.PLAYER_2, Position(1, 2))
    game.makePlay(Player.PLAYER_2, Position(4, 2))
    game.makePlay(Player.PLAYER_2, Position(3, 3))
    game.makePlay(Player.PLAYER_1, Position(2, 5))
    game.makePlay(Player.PLAYER_1, Position(4, 3))
    game.makePlay(Player.PLAYER_1, Position(3, 4))
    game.printBoard()
    print(game.getH())

# Call to main
main()


